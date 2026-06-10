using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class Profile : BaseEntity
{
    public Guid UserId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? AvatarUrl { get; set; }
    public string? PinHash { get; set; }
    public bool IsKidsProfile { get; set; }
    public User User { get; set; } = null!;
    public ICollection<WatchlistItem> WatchlistItems { get; set; } = new List<WatchlistItem>();
    public ICollection<WatchProgress> WatchProgresses { get; set; } = new List<WatchProgress>();
}
