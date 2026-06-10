using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class Episode : BaseEntity
{
    public Guid SeasonId { get; set; }
    public int EpisodeNumber { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public int DurationMinutes { get; set; }
    public string? ThumbnailUrl { get; set; }
    public Season Season { get; set; } = null!;
    public ICollection<VideoAsset> VideoAssets { get; set; } = new List<VideoAsset>();
    public ICollection<Subtitle> Subtitles { get; set; } = new List<Subtitle>();
}
