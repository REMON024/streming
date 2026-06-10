using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class SubtitleConfiguration : IEntityTypeConfiguration<Subtitle>
{
    public void Configure(EntityTypeBuilder<Subtitle> builder)
    {
        builder.ToTable("subtitles");
        builder.HasKey(s => s.Id);
        builder.Property(s => s.LanguageCode).HasMaxLength(10).IsRequired();
        builder.Property(s => s.LanguageName).HasMaxLength(100).IsRequired();
        builder.Property(s => s.FileUrl).HasMaxLength(1000).IsRequired();
        builder.HasIndex(s => s.ContentId);
        builder.HasIndex(s => s.EpisodeId);
    }
}
