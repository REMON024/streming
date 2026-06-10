using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Common;
using StreamingPlatform.Domain.Entities;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

    public DbSet<User> Users => Set<User>();
    public DbSet<Profile> Profiles => Set<Profile>();
    public DbSet<Subscription> Subscriptions => Set<Subscription>();
    public DbSet<Genre> Genres => Set<Genre>();
    public DbSet<Content> Contents => Set<Content>();
    public DbSet<ContentGenre> ContentGenres => Set<ContentGenre>();
    public DbSet<Season> Seasons => Set<Season>();
    public DbSet<Episode> Episodes => Set<Episode>();
    public DbSet<VideoAsset> VideoAssets => Set<VideoAsset>();
    public DbSet<Subtitle> Subtitles => Set<Subtitle>();
    public DbSet<WatchlistItem> WatchlistItems => Set<WatchlistItem>();
    public DbSet<WatchProgress> WatchProgresses => Set<WatchProgress>();
    public DbSet<Channel> Channels => Set<Channel>();
    public DbSet<LiveEvent> LiveEvents => Set<LiveEvent>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        modelBuilder.HasPostgresExtension("pg_trgm");
        SeedData(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        var now = DateTimeOffset.UtcNow;
        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {
            if (entry.State == EntityState.Modified)
            {
                entry.Entity.UpdatedAt = now;
            }
        }
        return await base.SaveChangesAsync(cancellationToken);
    }

    private static void SeedData(ModelBuilder modelBuilder)
    {
        var genres = new[]
        {
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000001"), Name = "Action", Slug = "action", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000002"), Name = "Drama", Slug = "drama", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000003"), Name = "Comedy", Slug = "comedy", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000004"), Name = "Sports", Slug = "sports", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000005"), Name = "Documentary", Slug = "documentary", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000006"), Name = "TV Shows", Slug = "tv-shows", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000007"), Name = "Horror", Slug = "horror", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000008"), Name = "Sci-Fi", Slug = "sci-fi", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000009"), Name = "Romance", Slug = "romance", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
            new Genre { Id = Guid.Parse("10000000-0000-0000-0000-000000000010"), Name = "Thriller", Slug = "thriller", CreatedAt = DateTimeOffset.UnixEpoch, UpdatedAt = DateTimeOffset.UnixEpoch },
        };

        modelBuilder.Entity<Genre>().HasData(genres);
    }
}
