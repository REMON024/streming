using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Domain.Entities;

public class Subscription : BaseEntity
{
    public Guid UserId { get; set; }
    public SubscriptionTier Tier { get; set; }
    public DateTimeOffset StartsAt { get; set; }
    public DateTimeOffset EndsAt { get; set; }
    public string? StripeSubscriptionId { get; set; }
    public User User { get; set; } = null!;
    public bool IsActive => DateTimeOffset.UtcNow < EndsAt;
}
