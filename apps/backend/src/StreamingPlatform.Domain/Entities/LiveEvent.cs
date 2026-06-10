using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Domain.Entities;

public class LiveEvent : BaseEntity
{
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? ThumbnailUrl { get; set; }
    public string? SportType { get; set; }
    public DateTimeOffset StartTime { get; set; }
    public DateTimeOffset? EndTime { get; set; }
    public LiveStreamStatus Status { get; set; }
    public string? HlsManifestPath { get; set; }
    public SubscriptionTier RequiredTier { get; set; }
    public bool IsFeatured { get; set; }
}
