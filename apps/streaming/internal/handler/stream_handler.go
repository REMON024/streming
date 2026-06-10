package handler

import (
	"bufio"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/go-chi/chi/v5"
	"streaming/internal/service"
	"go.uber.org/zap"
)

type StreamHandler struct {
	streamSvc *service.StreamService
	logger    *zap.Logger
}

func NewStreamHandler(svc *service.StreamService, logger *zap.Logger) *StreamHandler {
	return &StreamHandler{streamSvc: svc, logger: logger}
}

// ServeMasterManifest fetches the master.m3u8 from MinIO and rewrites variant
// playlist URIs so they route back through this service (token-bearing).
func (h *StreamHandler) ServeMasterManifest(w http.ResponseWriter, r *http.Request) {
	contentID := chi.URLParam(r, "contentId")
	token := extractTokenFromRequest(r)

	asset, err := h.streamSvc.ResolveContentAsset(r.Context(), contentID)
	if err != nil {
		http.Error(w, `{"error":"content not found"}`, http.StatusNotFound)
		return
	}

	content, err := h.streamSvc.FetchManifest(r.Context(), asset.MasterManifestPath)
	if err != nil {
		http.Error(w, `{"error":"manifest not available"}`, http.StatusServiceUnavailable)
		return
	}

	baseURL := fmt.Sprintf("/stream/%s", contentID)
	rewritten := rewriteMasterPlaylist(content, baseURL, token)

	w.Header().Set("Content-Type", "application/vnd.apple.mpegurl")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	fmt.Fprint(w, rewritten)
}

// ServeVariantManifest fetches a per-quality prog_index.m3u8 and rewrites
// .ts segment URIs to route through this service.
func (h *StreamHandler) ServeVariantManifest(w http.ResponseWriter, r *http.Request) {
	contentID := chi.URLParam(r, "contentId")
	quality := chi.URLParam(r, "quality")
	token := extractTokenFromRequest(r)

	asset, err := h.streamSvc.ResolveContentAsset(r.Context(), contentID)
	if err != nil {
		http.Error(w, `{"error":"content not found"}`, http.StatusNotFound)
		return
	}

	// MinIO path: videos-hls/{assetId}/{vN}/prog_index.m3u8
	manifestKey := fmt.Sprintf("videos-hls/%s/v%s/prog_index.m3u8", asset.AssetID, qualityIndex(quality))
	content, err := h.streamSvc.FetchManifest(r.Context(), manifestKey)
	if err != nil {
		http.Error(w, `{"error":"manifest not available"}`, http.StatusServiceUnavailable)
		return
	}

	baseURL := fmt.Sprintf("/stream/%s/%s", contentID, quality)
	rewritten := rewriteVariantPlaylist(content, baseURL, token)

	w.Header().Set("Content-Type", "application/vnd.apple.mpegurl")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	fmt.Fprint(w, rewritten)
}

// ServeSegment issues a redirect to a short-lived presigned MinIO URL for the
// requested .ts segment.
func (h *StreamHandler) ServeSegment(w http.ResponseWriter, r *http.Request) {
	contentID := chi.URLParam(r, "contentId")
	quality := chi.URLParam(r, "quality")
	segment := chi.URLParam(r, "segment")

	asset, err := h.streamSvc.ResolveContentAsset(r.Context(), contentID)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}

	segmentKey := fmt.Sprintf("videos-hls/%s/v%s/%s", asset.AssetID, qualityIndex(quality), segment)
	presignedURL, err := h.streamSvc.PresignSegmentURL(r.Context(), segmentKey, time.Hour)
	if err != nil {
		http.Error(w, `{"error":"segment not available"}`, http.StatusServiceUnavailable)
		return
	}

	http.Redirect(w, r, presignedURL, http.StatusFound)
}

// rewriteMasterPlaylist replaces relative variant playlist lines with absolute
// paths through this service, appending the token as a query param.
func rewriteMasterPlaylist(content, baseURL, token string) string {
	var sb strings.Builder
	scanner := bufio.NewScanner(strings.NewReader(content))
	for scanner.Scan() {
		line := scanner.Text()
		// Non-comment lines ending in .m3u8 are variant playlist references
		if !strings.HasPrefix(line, "#") && strings.HasSuffix(line, ".m3u8") {
			// e.g. "v0/prog_index.m3u8" → "/stream/{contentId}/v0/prog_index.m3u8?token=..."
			parts := strings.Split(strings.TrimSuffix(line, "/prog_index.m3u8"), "/")
			quality := parts[len(parts)-1] // "v0", "v1", "v2"
			line = fmt.Sprintf("%s/%s/prog_index.m3u8?token=%s", baseURL, quality, token)
		}
		sb.WriteString(line + "\n")
	}
	return sb.String()
}

// rewriteVariantPlaylist replaces relative .ts segment lines with absolute paths
// through this service, appending the token as a query param.
func rewriteVariantPlaylist(content, baseURL, token string) string {
	var sb strings.Builder
	scanner := bufio.NewScanner(strings.NewReader(content))
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.HasPrefix(line, "#") && strings.HasSuffix(line, ".ts") {
			line = fmt.Sprintf("%s/%s?token=%s", baseURL, line, token)
		}
		sb.WriteString(line + "\n")
	}
	return sb.String()
}

// qualityIndex maps human-readable quality names to the FFmpeg variant index
// used in the MinIO path (v0 = 360p, v1 = 720p, v2 = 1080p, v3 = 4k).
func qualityIndex(q string) string {
	switch q {
	case "360p":
		return "0"
	case "720p":
		return "1"
	case "1080p":
		return "2"
	case "4k":
		return "3"
	default:
		// Pass through "v0"/"v1"/"v2" or bare numeric indices unchanged
		return strings.TrimPrefix(q, "v")
	}
}

func extractTokenFromRequest(r *http.Request) string {
	auth := r.Header.Get("Authorization")
	if strings.HasPrefix(auth, "Bearer ") {
		return strings.TrimPrefix(auth, "Bearer ")
	}
	return r.URL.Query().Get("token")
}
