using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class Season : BaseEntity
{
    public Guid ContentId { get; set; }
    public int SeasonNumber { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public Content Content { get; set; } = null!;
    public ICollection<Episode> Episodes { get; set; } = new List<Episode>();
}
