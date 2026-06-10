using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class VideoAssetConfiguration : IEntityTypeConfiguration<VideoAsset>
{
    public void Configure(EntityTypeBuilder<VideoAsset> builder)
    {
        builder.ToTable("video_assets");
        builder.HasKey(v => v.Id);
        builder.Property(v => v.RawFilePath).HasMaxLength(1000).IsRequired();
        builder.Property(v => v.HlsManifestPath).HasMaxLength(1000);
        builder.HasIndex(v => v.ContentId);
        builder.HasIndex(v => v.EpisodeId);
        builder.HasIndex(v => v.Status);
    }
}
