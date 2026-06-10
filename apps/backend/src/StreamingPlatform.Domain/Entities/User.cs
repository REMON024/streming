using StreamingPlatform.Domain.Common;

namespace StreamingPlatform.Domain.Entities;

public class User : BaseEntity
{
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public bool IsAdmin { get; set; }
    public ICollection<Profile> Profiles { get; set; } = new List<Profile>();
    public ICollection<Subscription> Subscriptions { get; set; } = new List<Subscription>();
}
