package models

type TranscodeRequest struct {
	VideoAssetID string `json:"videoAssetId"`
	RawMinioPath string `json:"rawMinioPath"`
	ContentID    string `json:"contentId"`
}

type AssetStatusUpdate struct {
	Status          string `json:"status"`
	HlsManifestPath string `json:"hlsManifestPath"`
	ProcessedAt     string `json:"processedAt"`
}
