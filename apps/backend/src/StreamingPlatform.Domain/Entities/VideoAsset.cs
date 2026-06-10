using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Domain.Entities;

public class VideoAsset : BaseEntity
{
    public Guid? ContentId { get; set; }
    public Guid? EpisodeId { get; set; }
    public VideoQuality Quality { get; set; }
    public string? HlsManifestPath { get; set; }
    public string RawFilePath { get; set; } = string.Empty;
    public ProcessingStatus Status { get; set; }
    public long FileSizeBytes { get; set; }
    public int BitrateKbps { get; set; }
    public DateTimeOffset? ProcessedAt { get; set; }
    public Content? Content { get; set; }
    public Episode? Episode { get; set; }
}
