using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class GenreConfiguration : IEntityTypeConfiguration<Genre>
{
    public void Configure(EntityTypeBuilder<Genre> builder)
    {
        builder.ToTable("genres");
        builder.HasKey(g => g.Id);
        builder.Property(g => g.Name).HasMaxLength(100).IsRequired();
        builder.Property(g => g.Slug).HasMaxLength(100).IsRequired();
        builder.HasIndex(g => g.Slug).IsUnique();
    }
}
