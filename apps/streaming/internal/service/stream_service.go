package service

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"streaming/internal/cache"
	"streaming/internal/config"
	"streaming/internal/storage"
	"go.uber.org/zap"
)

type AssetInfo struct {
	AssetID            string
	MasterManifestPath string
	RequiredTier       int
}

type LiveEventInfo struct {
	ID              string
	HlsManifestPath string
	RequiredTier    int
	IsMinioPath     bool
	Status          string
}

type ChannelInfo struct {
	StreamURL    string
	RequiredTier int
}

type StreamService struct {
	cfg     *config.Config
	minio   *storage.MinioClient
	redis   *cache.RedisClient
	logger  *zap.Logger
	httpCli *http.Client
}

func NewStreamService(cfg *config.Config, minio *storage.MinioClient, redis *cache.RedisClient, logger *zap.Logger) *StreamService {
	return &StreamService{
		cfg:     cfg,
		minio:   minio,
		redis:   redis,
		logger:  logger,
		httpCli: &http.Client{Timeout: 5 * time.Second},
	}
}

func (s *StreamService) ResolveContentAsset(ctx context.Context, contentID string) (*AssetInfo, error) {
	cacheKey := fmt.Sprintf("stream:asset:%s", contentID)
	if cached, err := s.redis.Get(ctx, cacheKey); err == nil {
		var info AssetInfo
		if json.Unmarshal([]byte(cached), &info) == nil {
			return &info, nil
		}
	}

	url := fmt.Sprintf("%s/api/content/%s/stream", s.cfg.BackendURL, contentID)
	resp, err := s.httpCli.Get(url)
	if err != nil || resp.StatusCode != 200 {
		return nil, fmt.Errorf("content not found: %s", contentID)
	}
	defer resp.Body.Close()

	var streamInfo struct {
		AssetID        string `json:"assetId"`
		MasterM3u8Path string `json:"masterM3u8Path"`
		RequiredTier   int    `json:"requiredTier"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&streamInfo); err != nil {
		return nil, err
	}

	info := &AssetInfo{
		AssetID:            streamInfo.AssetID,
		MasterManifestPath: streamInfo.MasterM3u8Path,
		RequiredTier:       streamInfo.RequiredTier,
	}

	if data, err := json.Marshal(info); err == nil {
		s.redis.Set(ctx, cacheKey, string(data), 5*time.Minute)
	}
	return info, nil
}

func (s *StreamService) FetchManifest(ctx context.Context, minioKey string) (string, error) {
	obj, err := s.minio.GetObject("videos-hls", minioKey)
	if err != nil {
		return "", err
	}
	defer obj.Close()
	data, err := io.ReadAll(obj)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (s *StreamService) PresignSegmentURL(ctx context.Context, minioKey string, expiry time.Duration) (string, error) {
	return s.minio.PresignedGetURL("videos-hls", minioKey, expiry)
}

func (s *StreamService) ResolveLiveEvent(ctx context.Context, eventID string) (*LiveEventInfo, error) {
	cacheKey := fmt.Sprintf("stream:live:%s", eventID)
	if cached, err := s.redis.Get(ctx, cacheKey); err == nil {
		var info LiveEventInfo
		if json.Unmarshal([]byte(cached), &info) == nil {
			return &info, nil
		}
	}

	url := fmt.Sprintf("%s/api/live/%s", s.cfg.BackendURL, eventID)
	resp, err := s.httpCli.Get(url)
	if err != nil || resp.StatusCode != 200 {
		return nil, fmt.Errorf("live event not found: %s", eventID)
	}
	defer resp.Body.Close()

	var eventInfo struct {
		HlsManifestPath string `json:"hlsManifestPath"`
		RequiredTier    int    `json:"requiredTier"`
		Status          string `json:"status"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&eventInfo); err != nil {
		return nil, err
	}

	info := &LiveEventInfo{
		ID:              eventID,
		HlsManifestPath: eventInfo.HlsManifestPath,
		RequiredTier:    eventInfo.RequiredTier,
		Status:          eventInfo.Status,
		IsMinioPath:     !isExternalURL(eventInfo.HlsManifestPath),
	}

	if data, err := json.Marshal(info); err == nil {
		s.redis.Set(ctx, cacheKey, string(data), 30*time.Second) // short TTL for live
	}
	return info, nil
}

func (s *StreamService) ResolveChannel(ctx context.Context, channelSlug string) (*ChannelInfo, error) {
	cacheKey := fmt.Sprintf("stream:channel:%s", channelSlug)
	if cached, err := s.redis.Get(ctx, cacheKey); err == nil {
		var info ChannelInfo
		if json.Unmarshal([]byte(cached), &info) == nil {
			return &info, nil
		}
	}

	url := fmt.Sprintf("%s/api/channels/%s", s.cfg.BackendURL, channelSlug)
	resp, err := s.httpCli.Get(url)
	if err != nil || resp.StatusCode != 200 {
		return nil, fmt.Errorf("channel not found: %s", channelSlug)
	}
	defer resp.Body.Close()

	var ch struct {
		StreamURL    string `json:"streamUrl"`
		RequiredTier int    `json:"requiredTier"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&ch); err != nil {
		return nil, err
	}

	info := &ChannelInfo{StreamURL: ch.StreamURL, RequiredTier: ch.RequiredTier}
	if data, err := json.Marshal(info); err == nil {
		s.redis.Set(ctx, cacheKey, string(data), 5*time.Minute)
	}
	return info, nil
}

func isExternalURL(s string) bool {
	return len(s) >= 7 && (s[:7] == "http://" || (len(s) >= 8 && s[:8] == "https://"))
}
