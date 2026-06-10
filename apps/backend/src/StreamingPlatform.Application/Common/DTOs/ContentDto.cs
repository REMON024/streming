using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Application.Common.DTOs;

public class VideoAssetDto
{
    public Guid Id { get; set; }
    public VideoQuality Quality { get; set; }
    public string? HlsManifestPath { get; set; }
    public ProcessingStatus Status { get; set; }
    public long FileSizeBytes { get; set; }
    public int BitrateKbps { get; set; }
}

public class EpisodeDto
{
    public Guid Id { get; set; }
    public int EpisodeNumber { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public int DurationMinutes { get; set; }
    public string? ThumbnailUrl { get; set; }
    public List<VideoAssetDto> VideoAssets { get; set; } = new();
    public List<SubtitleDto> Subtitles { get; set; } = new();
}

public class SeasonDto
{
    public Guid Id { get; set; }
    public int SeasonNumber { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public List<EpisodeDto> Episodes { get; set; } = new();
}

public class ContentSummaryDto
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string? ThumbnailUrl { get; set; }
    public string? BackdropUrl { get; set; }
    public ContentType Type { get; set; }
    public int ReleaseYear { get; set; }
    public int DurationMinutes { get; set; }
    public SubscriptionTier RequiredTier { get; set; }
    public decimal AverageRating { get; set; }
    public bool IsFeatured { get; set; }
    public bool IsTrending { get; set; }
}

public class ContentDetailDto : ContentSummaryDto
{
    public string Description { get; set; } = string.Empty;
    public List<GenreDto> Genres { get; set; } = new();
    public List<SeasonDto> Seasons { get; set; } = new();
    public List<VideoAssetDto> VideoAssets { get; set; } = new();
    public List<SubtitleDto> Subtitles { get; set; } = new();
}
