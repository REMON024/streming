package handler

import (
	"encoding/json"
	"net/http"

	"streaming/internal/transcoder"
	"streaming/pkg/models"
	"go.uber.org/zap"
)

type TranscodeHandler struct {
	pool   *transcoder.WorkerPool
	logger *zap.Logger
}

func NewTranscodeHandler(pool *transcoder.WorkerPool, logger *zap.Logger) *TranscodeHandler {
	return &TranscodeHandler{pool: pool, logger: logger}
}

func (h *TranscodeHandler) Enqueue(w http.ResponseWriter, r *http.Request) {
	var req models.TranscodeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if req.VideoAssetID == "" || req.RawMinioPath == "" {
		http.Error(w, `{"error":"videoAssetId and rawMinioPath are required"}`, http.StatusBadRequest)
		return
	}
	h.pool.Enqueue(transcoder.TranscodeJob{
		VideoAssetID: req.VideoAssetID,
		RawMinioPath: req.RawMinioPath,
		ContentID:    req.ContentID,
	})
	h.logger.Info("transcode job enqueued", zap.String("assetId", req.VideoAssetID))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(map[string]string{"status": "accepted", "videoAssetId": req.VideoAssetID})
}
