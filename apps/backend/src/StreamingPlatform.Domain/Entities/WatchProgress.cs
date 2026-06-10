using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class WatchProgress : BaseEntity
{
    public Guid ProfileId { get; set; }
    public Guid? ContentId { get; set; }
    public Guid? EpisodeId { get; set; }
    public int PositionSeconds { get; set; }
    public int TotalDurationSeconds { get; set; }
    public bool IsCompleted { get; set; }
    public DateTimeOffset LastWatchedAt { get; set; } = DateTimeOffset.UtcNow;
    public Profile Profile { get; set; } = null!;
    public Content? Content { get; set; }
}
