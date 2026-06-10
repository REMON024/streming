using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<User> Users { get; }
    DbSet<Profile> Profiles { get; }
    DbSet<Subscription> Subscriptions { get; }
    DbSet<Genre> Genres { get; }
    DbSet<Content> Contents { get; }
    DbSet<ContentGenre> ContentGenres { get; }
    DbSet<Season> Seasons { get; }
    DbSet<Episode> Episodes { get; }
    DbSet<VideoAsset> VideoAssets { get; }
    DbSet<Subtitle> Subtitles { get; }
    DbSet<WatchlistItem> WatchlistItems { get; }
    DbSet<WatchProgress> WatchProgresses { get; }
    DbSet<Channel> Channels { get; }
    DbSet<LiveEvent> LiveEvents { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
