using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class WatchlistItem : BaseEntity
{
    public Guid ProfileId { get; set; }
    public Guid ContentId { get; set; }
    public DateTimeOffset AddedAt { get; set; } = DateTimeOffset.UtcNow;
    public Profile Profile { get; set; } = null!;
    public Content Content { get; set; } = null!;
}
