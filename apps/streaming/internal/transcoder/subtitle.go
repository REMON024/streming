package transcoder

import (
	"strings"
)

// ConvertSRTtoVTT converts SRT subtitle content to WebVTT format.
// It replaces the SRT comma decimal separator in timestamps with a period
// and prepends the required WEBVTT header.
func ConvertSRTtoVTT(srtContent string) string {
	// Normalize line endings first
	result := strings.ReplaceAll(srtContent, "\r\n", "\n")
	// Replace SRT timestamp decimal separator (comma) with the VTT period
	result = strings.ReplaceAll(result, ",", ".")
	return "WEBVTT\n\n" + result
}
