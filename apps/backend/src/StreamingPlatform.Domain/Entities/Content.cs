using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Domain.Entities;

public class Content : BaseEntity
{
    public string Title { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? ThumbnailUrl { get; set; }
    public string? BackdropUrl { get; set; }
    public int ReleaseYear { get; set; }
    public int DurationMinutes { get; set; }
    public ContentType Type { get; set; }
    public SubscriptionTier RequiredTier { get; set; }
    public bool IsPublished { get; set; }
    public bool IsFeatured { get; set; }
    public bool IsTrending { get; set; }
    public decimal AverageRating { get; set; }
    public ICollection<ContentGenre> ContentGenres { get; set; } = new List<ContentGenre>();
    public ICollection<Season> Seasons { get; set; } = new List<Season>();
    public ICollection<VideoAsset> VideoAssets { get; set; } = new List<VideoAsset>();
    public ICollection<Subtitle> Subtitles { get; set; } = new List<Subtitle>();
    public ICollection<WatchlistItem> WatchlistItems { get; set; } = new List<WatchlistItem>();
    public ICollection<WatchProgress> WatchProgresses { get; set; } = new List<WatchProgress>();
}
