using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class SeasonConfiguration : IEntityTypeConfiguration<Season>
{
    public void Configure(EntityTypeBuilder<Season> builder)
    {
        builder.ToTable("seasons");
        builder.HasKey(s => s.Id);
        builder.Property(s => s.Title).HasMaxLength(200).IsRequired();
        builder.Property(s => s.Description).HasMaxLength(1000);
        builder.HasIndex(s => new { s.ContentId, s.SeasonNumber }).IsUnique();

        builder.HasMany(s => s.Episodes)
            .WithOne(e => e.Season)
            .HasForeignKey(e => e.SeasonId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
