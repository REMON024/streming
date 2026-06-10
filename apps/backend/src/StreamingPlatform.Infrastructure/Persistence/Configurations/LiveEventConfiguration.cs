using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class LiveEventConfiguration : IEntityTypeConfiguration<LiveEvent>
{
    public void Configure(EntityTypeBuilder<LiveEvent> builder)
    {
        builder.ToTable("live_events");
        builder.HasKey(e => e.Id);
        builder.Property(e => e.Title).HasMaxLength(300).IsRequired();
        builder.Property(e => e.Description).HasMaxLength(2000);
        builder.Property(e => e.ThumbnailUrl).HasMaxLength(500);
        builder.Property(e => e.SportType).HasMaxLength(100);
        builder.Property(e => e.HlsManifestPath).HasMaxLength(1000);
        builder.HasIndex(e => e.Status);
        builder.HasIndex(e => e.StartTime);
        builder.HasIndex(e => e.IsFeatured);
    }
}
