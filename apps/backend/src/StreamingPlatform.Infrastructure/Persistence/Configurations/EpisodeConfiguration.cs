using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class EpisodeConfiguration : IEntityTypeConfiguration<Episode>
{
    public void Configure(EntityTypeBuilder<Episode> builder)
    {
        builder.ToTable("episodes");
        builder.HasKey(e => e.Id);
        builder.Property(e => e.Title).HasMaxLength(300).IsRequired();
        builder.Property(e => e.Description).HasMaxLength(2000);
        builder.Property(e => e.ThumbnailUrl).HasMaxLength(500);
        builder.HasIndex(e => new { e.SeasonId, e.EpisodeNumber }).IsUnique();

        builder.HasMany(e => e.VideoAssets)
            .WithOne(v => v.Episode)
            .HasForeignKey(v => v.EpisodeId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(e => e.Subtitles)
            .WithOne(s => s.Episode)
            .HasForeignKey(s => s.EpisodeId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
