package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"streaming/internal/cache"
	"streaming/internal/config"
	"streaming/internal/server"
	"streaming/internal/service"
	"streaming/internal/storage"
	"streaming/internal/transcoder"

	"go.uber.org/zap"
)

func main() {
	cfg := config.Load()

	logger, _ := zap.NewProduction()
	defer logger.Sync()

	minioClient := storage.NewMinioClient(cfg, logger)
	redisClient := cache.NewRedisClient(cfg, logger)

	transcodeService := service.NewTranscodeService(cfg, minioClient, redisClient, logger)
	pool := transcoder.NewWorkerPool(cfg.MaxTranscodeWorkers, transcodeService, logger)

	streamService := service.NewStreamService(cfg, minioClient, redisClient, logger)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	pool.Start(ctx)

	r := server.NewRouter(cfg, streamService, transcodeService, pool, logger)

	srv := &http.Server{
		Addr:    ":" + cfg.Port,
		Handler: r,
	}

	go func() {
		logger.Info("streaming service starting", zap.String("port", cfg.Port))
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatal("server error", zap.Error(err))
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	shutCtx, shutCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutCancel()
	srv.Shutdown(shutCtx)
	logger.Info("streaming service stopped")
}
