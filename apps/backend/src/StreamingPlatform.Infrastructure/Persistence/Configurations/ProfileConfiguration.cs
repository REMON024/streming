using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class ProfileConfiguration : IEntityTypeConfiguration<Profile>
{
    public void Configure(EntityTypeBuilder<Profile> builder)
    {
        builder.ToTable("profiles");
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Name).HasMaxLength(50).IsRequired();
        builder.Property(p => p.AvatarUrl).HasMaxLength(500);
        builder.Property(p => p.PinHash).HasMaxLength(200);

        builder.HasMany(p => p.WatchlistItems)
            .WithOne(w => w.Profile)
            .HasForeignKey(w => w.ProfileId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(p => p.WatchProgresses)
            .WithOne(w => w.Profile)
            .HasForeignKey(w => w.ProfileId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
