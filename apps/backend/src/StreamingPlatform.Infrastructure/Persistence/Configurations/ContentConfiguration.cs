using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class ContentConfiguration : IEntityTypeConfiguration<Content>
{
    public void Configure(EntityTypeBuilder<Content> builder)
    {
        builder.ToTable("content");
        builder.HasKey(c => c.Id);
        builder.Property(c => c.Title).HasMaxLength(300).IsRequired();
        builder.Property(c => c.Slug).HasMaxLength(300).IsRequired();
        builder.Property(c => c.Description).IsRequired();
        builder.Property(c => c.ThumbnailUrl).HasMaxLength(500);
        builder.Property(c => c.BackdropUrl).HasMaxLength(500);
        builder.Property(c => c.AverageRating).HasPrecision(3, 1);

        builder.HasIndex(c => c.Slug).IsUnique();
        builder.HasIndex(c => c.IsFeatured);
        builder.HasIndex(c => c.IsTrending);
        builder.HasIndex(c => c.IsPublished);
        builder.HasIndex(c => c.Type);

        builder.Property<string>("SearchVector")
            .HasColumnType("tsvector")
            .HasComputedColumnSql(
                "to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,''))",
                stored: true);
        builder.HasIndex("SearchVector").HasMethod("GIN");

        builder.HasMany(c => c.Seasons)
            .WithOne(s => s.Content)
            .HasForeignKey(s => s.ContentId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(c => c.VideoAssets)
            .WithOne(v => v.Content)
            .HasForeignKey(v => v.ContentId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(c => c.Subtitles)
            .WithOne(s => s.Content)
            .HasForeignKey(s => s.ContentId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(c => c.WatchlistItems)
            .WithOne(w => w.Content)
            .HasForeignKey(w => w.ContentId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(c => c.WatchProgresses)
            .WithOne(w => w.Content)
            .HasForeignKey(w => w.ContentId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
