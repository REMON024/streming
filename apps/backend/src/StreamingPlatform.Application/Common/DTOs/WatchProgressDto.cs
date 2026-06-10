namespace StreamingPlatform.Application.Common.DTOs;

public class WatchProgressDto
{
    public Guid? ContentId { get; set; }
    public Guid? EpisodeId { get; set; }
    public int PositionSeconds { get; set; }
    public int TotalDurationSeconds { get; set; }
    public bool IsCompleted { get; set; }
    public DateTimeOffset LastWatchedAt { get; set; }
}
