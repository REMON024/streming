package service

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"streaming/internal/cache"
	"streaming/internal/config"
	"streaming/internal/storage"
	"streaming/internal/transcoder"
	"go.uber.org/zap"
)

type TranscodeService struct {
	cfg     *config.Config
	minio   *storage.MinioClient
	redis   *cache.RedisClient
	logger  *zap.Logger
	httpCli *http.Client
}

func NewTranscodeService(cfg *config.Config, minio *storage.MinioClient, redis *cache.RedisClient, logger *zap.Logger) *TranscodeService {
	return &TranscodeService{
		cfg:     cfg,
		minio:   minio,
		redis:   redis,
		logger:  logger,
		httpCli: &http.Client{Timeout: 30 * time.Second},
	}
}

// ProcessJob implements transcoder.JobProcessor.
func (s *TranscodeService) ProcessJob(ctx context.Context, job transcoder.TranscodeJob) error {
	s.logger.Info("processing transcode job", zap.String("assetId", job.VideoAssetID))

	// Create temp working directory
	tmpDir, err := os.MkdirTemp("", "transcode-"+job.VideoAssetID)
	if err != nil {
		return fmt.Errorf("create temp dir: %w", err)
	}
	defer os.RemoveAll(tmpDir)

	// Download raw video from MinIO
	rawPath := filepath.Join(tmpDir, "original.mp4")
	if err := s.minio.FGetObject("videos-raw", job.RawMinioPath, rawPath); err != nil {
		return fmt.Errorf("download raw video: %w", err)
	}
	s.logger.Info("downloaded raw video", zap.String("path", rawPath))

	// Prepare HLS output directory
	outputDir := filepath.Join(tmpDir, "hls")
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		return fmt.Errorf("create hls output dir: %w", err)
	}

	input := transcoder.TranscodeInput{
		InputPath: rawPath,
		OutputDir: outputDir,
		AssetID:   job.VideoAssetID,
	}

	generatedFiles, err := transcoder.RunPipeline(ctx, input, s.logger)
	if err != nil {
		s.notifyStatus(ctx, job.VideoAssetID, "failed", "")
		return fmt.Errorf("transcode failed: %w", err)
	}
	s.logger.Info("transcoding complete", zap.Int("files", len(generatedFiles)))

	// Upload all HLS files to MinIO
	for _, f := range generatedFiles {
		if err := s.minio.FPutObject("videos-hls", f.MinioKey, f.LocalPath, f.ContentType); err != nil {
			return fmt.Errorf("upload %s: %w", f.MinioKey, err)
		}
	}
	s.logger.Info("uploaded HLS files to MinIO")

	// Invalidate stream cache for this content ID
	if job.ContentID != "" {
		cacheKey := fmt.Sprintf("stream:asset:%s", job.ContentID)
		s.redis.Del(ctx, cacheKey)
	}

	// Notify backend of completion
	manifestPath := fmt.Sprintf("videos-hls/%s/master.m3u8", job.VideoAssetID)
	return s.notifyStatus(ctx, job.VideoAssetID, "ready", manifestPath)
}

func (s *TranscodeService) notifyStatus(ctx context.Context, assetID, status, manifestPath string) error {
	payload := map[string]string{
		"status":          status,
		"hlsManifestPath": manifestPath,
		"processedAt":     time.Now().UTC().Format(time.RFC3339),
	}
	body, _ := json.Marshal(payload)

	url := fmt.Sprintf("%s/api/admin/assets/%s/status", s.cfg.BackendURL, assetID)
	req, err := http.NewRequestWithContext(ctx, http.MethodPatch, url, bytes.NewReader(body))
	if err != nil {
		return fmt.Errorf("build notify request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Internal-Key", s.cfg.InternalAPIKey)

	resp, err := s.httpCli.Do(req)
	if err != nil {
		s.logger.Error("failed to notify backend", zap.Error(err))
		return err
	}
	defer resp.Body.Close()
	s.logger.Info("notified backend of transcode status",
		zap.String("status", status),
		zap.Int("httpStatus", resp.StatusCode))
	return nil
}
