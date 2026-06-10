package handler

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
	"streaming/internal/service"
	"go.uber.org/zap"
)

type LiveHandler struct {
	streamSvc *service.StreamService
	logger    *zap.Logger
}

func NewLiveHandler(svc *service.StreamService, logger *zap.Logger) *LiveHandler {
	return &LiveHandler{streamSvc: svc, logger: logger}
}

// ServeEventManifest resolves the live event and either serves its HLS manifest
// directly (MinIO-hosted) or redirects to the external CDN URL.
func (h *LiveHandler) ServeEventManifest(w http.ResponseWriter, r *http.Request) {
	eventID := chi.URLParam(r, "eventId")
	token := extractTokenFromRequest(r)
	_ = token // validated by middleware; kept for future per-event token pinning

	liveInfo, err := h.streamSvc.ResolveLiveEvent(r.Context(), eventID)
	if err != nil {
		http.Error(w, `{"error":"event not found"}`, http.StatusNotFound)
		return
	}
	if liveInfo.HlsManifestPath == "" {
		http.Error(w, `{"error":"stream not available"}`, http.StatusServiceUnavailable)
		return
	}

	if liveInfo.IsMinioPath {
		content, err := h.streamSvc.FetchManifest(r.Context(), liveInfo.HlsManifestPath)
		if err != nil {
			http.Error(w, `{"error":"manifest not available"}`, http.StatusServiceUnavailable)
			return
		}
		w.Header().Set("Content-Type", "application/vnd.apple.mpegurl")
		w.Header().Set("Cache-Control", "no-cache")
		fmt.Fprint(w, content)
		return
	}

	// External live stream — redirect the player directly to the CDN URL
	http.Redirect(w, r, liveInfo.HlsManifestPath, http.StatusFound)
}

// ServeChannelManifest returns the stream URL for a linear TV channel.
func (h *LiveHandler) ServeChannelManifest(w http.ResponseWriter, r *http.Request) {
	channelSlug := chi.URLParam(r, "channelSlug")

	channelInfo, err := h.streamSvc.ResolveChannel(r.Context(), channelSlug)
	if err != nil {
		http.Error(w, `{"error":"channel not found"}`, http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"streamUrl": channelInfo.StreamURL})
}
