using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class WatchProgressConfiguration : IEntityTypeConfiguration<WatchProgress>
{
    public void Configure(EntityTypeBuilder<WatchProgress> builder)
    {
        builder.ToTable("watch_progress");
        builder.HasKey(w => w.Id);
        builder.HasIndex(w => new { w.ProfileId, w.ContentId, w.EpisodeId });
        builder.HasIndex(w => w.ProfileId);
        builder.HasIndex(w => w.LastWatchedAt);
    }
}
