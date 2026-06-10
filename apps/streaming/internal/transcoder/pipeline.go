package transcoder

import (
	"context"
	"fmt"
	"os"
	"path/filepath"

	"go.uber.org/zap"
)

type GeneratedFile struct {
	LocalPath   string
	MinioKey    string
	ContentType string
}

// RunPipeline orchestrates multi-bitrate HLS transcoding and returns all
// generated files ready for upload to MinIO.
func RunPipeline(ctx context.Context, input TranscodeInput, logger *zap.Logger) ([]GeneratedFile, error) {
	// Create per-variant output subdirectories
	for _, v := range []string{"v0", "v1", "v2"} {
		if err := os.MkdirAll(filepath.Join(input.OutputDir, v), 0755); err != nil {
			return nil, fmt.Errorf("create output dir %s: %w", v, err)
		}
	}

	args := BuildFFmpegArgs(input)
	if err := RunFFmpeg(ctx, args, logger); err != nil {
		return nil, err
	}

	var files []GeneratedFile

	// Master playlist
	masterLocal := filepath.Join(input.OutputDir, "master.m3u8")
	files = append(files, GeneratedFile{
		LocalPath:   masterLocal,
		MinioKey:    fmt.Sprintf("videos-hls/%s/master.m3u8", input.AssetID),
		ContentType: "application/vnd.apple.mpegurl",
	})

	// Per-variant files (playlist + .ts segments)
	for _, variant := range []string{"v0", "v1", "v2"} {
		varDir := filepath.Join(input.OutputDir, variant)

		// Variant playlist
		files = append(files, GeneratedFile{
			LocalPath:   filepath.Join(varDir, "prog_index.m3u8"),
			MinioKey:    fmt.Sprintf("videos-hls/%s/%s/prog_index.m3u8", input.AssetID, variant),
			ContentType: "application/vnd.apple.mpegurl",
		})

		// .ts segments
		entries, err := os.ReadDir(varDir)
		if err != nil {
			return nil, fmt.Errorf("read dir %s: %w", varDir, err)
		}
		for _, entry := range entries {
			if filepath.Ext(entry.Name()) == ".ts" {
				files = append(files, GeneratedFile{
					LocalPath:   filepath.Join(varDir, entry.Name()),
					MinioKey:    fmt.Sprintf("videos-hls/%s/%s/%s", input.AssetID, variant, entry.Name()),
					ContentType: "video/MP2T",
				})
			}
		}
	}

	return files, nil
}
