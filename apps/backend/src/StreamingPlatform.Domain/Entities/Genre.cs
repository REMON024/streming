using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class Genre : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public ICollection<ContentGenre> ContentGenres { get; set; } = new List<ContentGenre>();
}
