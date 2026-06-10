package transcoder

import (
	"context"
	"fmt"
	"os/exec"

	"go.uber.org/zap"
)

type TranscodeInput struct {
	InputPath string
	OutputDir string
	AssetID   string
}

// BuildFFmpegArgs produces a single FFmpeg command that outputs 3 HLS variants.
// Output: {OutputDir}/master.m3u8, {OutputDir}/v0/, v1/, v2/
func BuildFFmpegArgs(input TranscodeInput) []string {
	return []string{
		"ffmpeg", "-y",
		"-i", input.InputPath,
		"-filter_complex",
		"[0:v]split=3[v1][v2][v3];" +
			"[v1]scale=w=640:h=360:force_original_aspect_ratio=decrease[v360];" +
			"[v2]scale=w=1280:h=720:force_original_aspect_ratio=decrease[v720];" +
			"[v3]scale=w=1920:h=1080:force_original_aspect_ratio=decrease[v1080]",
		// 360p
		"-map", "[v360]", "-map", "0:a:0",
		"-c:v:0", "libx264", "-b:v:0", "800k", "-maxrate:v:0", "856k", "-bufsize:v:0", "1200k",
		"-c:a:0", "aac", "-b:a:0", "96k", "-ac", "2",
		// 720p
		"-map", "[v720]", "-map", "0:a:0",
		"-c:v:1", "libx264", "-b:v:1", "2800k", "-maxrate:v:1", "2996k", "-bufsize:v:1", "4200k",
		"-c:a:1", "aac", "-b:a:1", "128k", "-ac", "2",
		// 1080p
		"-map", "[v1080]", "-map", "0:a:0",
		"-c:v:2", "libx264", "-b:v:2", "5000k", "-maxrate:v:2", "5350k", "-bufsize:v:2", "7500k",
		"-c:a:2", "aac", "-b:a:2", "192k", "-ac", "2",
		// HLS settings
		"-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2",
		"-master_pl_name", "master.m3u8",
		"-f", "hls",
		"-hls_time", "6",
		"-hls_playlist_type", "vod",
		"-hls_flags", "independent_segments",
		"-hls_segment_type", "mpegts",
		"-hls_segment_filename", fmt.Sprintf("%s/v%%v/seg%%03d.ts", input.OutputDir),
		fmt.Sprintf("%s/v%%v/prog_index.m3u8", input.OutputDir),
	}
}

// RunFFmpeg executes the FFmpeg command and logs combined output via zap.
func RunFFmpeg(ctx context.Context, args []string, logger *zap.Logger) error {
	cmd := exec.CommandContext(ctx, args[0], args[1:]...)
	output, err := cmd.CombinedOutput()
	if err != nil {
		logger.Error("ffmpeg failed", zap.String("output", string(output)), zap.Error(err))
		return fmt.Errorf("ffmpeg error: %w\noutput: %s", err, output)
	}
	logger.Info("ffmpeg completed successfully")
	return nil
}
