namespace StreamingPlatform.Domain.Entities;

public class ContentGenre
{
    public Guid ContentId { get; set; }
    public Guid GenreId { get; set; }
    public Content Content { get; set; } = null!;
    public Genre Genre { get; set; } = null!;
}
