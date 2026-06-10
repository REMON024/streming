using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Domain.Entities;

public class Channel : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? LogoUrl { get; set; }
    public string StreamUrl { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public SubscriptionTier RequiredTier { get; set; }
    public bool IsActive { get; set; } = true;
    public int SortOrder { get; set; }
}
