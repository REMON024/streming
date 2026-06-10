using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Application.Common.DTOs;

public class ChannelDto
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string? LogoUrl { get; set; }
    public string Category { get; set; } = string.Empty;
    public string StreamUrl { get; set; } = string.Empty;
    public SubscriptionTier RequiredTier { get; set; }
}
