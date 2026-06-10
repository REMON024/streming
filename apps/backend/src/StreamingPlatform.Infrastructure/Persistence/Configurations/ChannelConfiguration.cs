using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class ChannelConfiguration : IEntityTypeConfiguration<Channel>
{
    public void Configure(EntityTypeBuilder<Channel> builder)
    {
        builder.ToTable("channels");
        builder.HasKey(c => c.Id);
        builder.Property(c => c.Name).HasMaxLength(200).IsRequired();
        builder.Property(c => c.Slug).HasMaxLength(200).IsRequired();
        builder.Property(c => c.Description).HasMaxLength(1000);
        builder.Property(c => c.LogoUrl).HasMaxLength(500);
        builder.Property(c => c.StreamUrl).HasMaxLength(1000).IsRequired();
        builder.Property(c => c.Category).HasMaxLength(100).IsRequired();
        builder.HasIndex(c => c.Slug).IsUnique();
        builder.HasIndex(c => new { c.IsActive, c.SortOrder });
    }
}
