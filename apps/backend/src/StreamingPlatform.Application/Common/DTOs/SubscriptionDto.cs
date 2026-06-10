using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Application.Common.DTOs;

public class SubscriptionDto
{
    public Guid Id { get; set; }
    public SubscriptionTier Tier { get; set; }
    public DateTimeOffset StartsAt { get; set; }
    public DateTimeOffset EndsAt { get; set; }
    public bool IsActive { get; set; }
    public string? StripeSubscriptionId { get; set; }
}
