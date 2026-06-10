using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class Subtitle : BaseEntity
{
    public Guid? ContentId { get; set; }
    public Guid? EpisodeId { get; set; }
    public string LanguageCode { get; set; } = string.Empty;
    public string LanguageName { get; set; } = string.Empty;
    public string FileUrl { get; set; } = string.Empty;
    public Content? Content { get; set; }
    public Episode? Episode { get; set; }
}
