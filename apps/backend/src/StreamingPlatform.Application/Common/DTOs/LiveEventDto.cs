using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Application.Common.DTOs;

public class LiveEventDto
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? ThumbnailUrl { get; set; }
    public string? SportType { get; set; }
    public DateTimeOffset StartTime { get; set; }
    public DateTimeOffset? EndTime { get; set; }
    public LiveStreamStatus Status { get; set; }
    public SubscriptionTier RequiredTier { get; set; }
    public bool IsFeatured { get; set; }
    public string? StreamUrl { get; set; }
}
