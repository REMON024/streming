package server

import (
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	chimiddleware "github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"

	"streaming/internal/config"
	"streaming/internal/handler"
	"streaming/internal/middleware"
	"streaming/internal/service"
	"streaming/internal/transcoder"
	"go.uber.org/zap"
)

// NewRouter wires up all HTTP routes and returns the configured chi router.
func NewRouter(
	cfg *config.Config,
	streamSvc *service.StreamService,
	transcodesSvc *service.TranscodeService,
	pool *transcoder.WorkerPool,
	logger *zap.Logger,
) http.Handler {
	r := chi.NewRouter()

	// Global middleware
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-Internal-Key"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: false,
		MaxAge:           300,
	}))
	r.Use(chimiddleware.RequestID)
	r.Use(chimiddleware.RealIP)
	r.Use(zapLoggerMiddleware(logger))
	r.Use(chimiddleware.Recoverer)

	// Instantiate handlers
	streamHandler := handler.NewStreamHandler(streamSvc, logger)
	transcodeHandler := handler.NewTranscodeHandler(pool, logger)
	liveHandler := handler.NewLiveHandler(streamSvc, logger)

	// Routes
	r.Get("/health", handler.HealthHandler)

	// VOD streaming routes — JWT required
	r.Group(func(r chi.Router) {
		r.Use(middleware.RequireJWT(cfg))
		r.Get("/stream/{contentId}/master.m3u8", streamHandler.ServeMasterManifest)
		r.Get("/stream/{contentId}/{quality}/prog_index.m3u8", streamHandler.ServeVariantManifest)
	})

	// Segment route — JWT accepted from query param (?token=) for HLS player compatibility
	r.With(middleware.RequireJWTFromQuery(cfg)).
		Get("/stream/{contentId}/{quality}/{segment}", streamHandler.ServeSegment)

	// Internal transcode enqueue — service-to-service key auth
	r.With(middleware.RequireInternalKey(cfg)).
		Post("/internal/transcode", transcodeHandler.Enqueue)

	// Live event stream — JWT required
	r.With(middleware.RequireJWT(cfg)).
		Get("/live/{eventId}/master.m3u8", liveHandler.ServeEventManifest)

	// Linear TV channel stream — JWT required
	r.With(middleware.RequireJWT(cfg)).
		Get("/channel/{channelSlug}/stream.m3u8", liveHandler.ServeChannelManifest)

	return r
}

// zapLoggerMiddleware is a minimal chi-compatible request logger backed by zap.
func zapLoggerMiddleware(logger *zap.Logger) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			ww := chimiddleware.NewWrapResponseWriter(w, r.ProtoMajor)
			next.ServeHTTP(ww, r)
			logger.Info("request",
				zap.String("method", r.Method),
				zap.String("path", r.URL.Path),
				zap.Int("status", ww.Status()),
				zap.Duration("latency", time.Since(start)),
				zap.String("requestId", chimiddleware.GetReqID(r.Context())),
			)
		})
	}
}
