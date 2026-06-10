using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class SubscriptionConfiguration : IEntityTypeConfiguration<Subscription>
{
    public void Configure(EntityTypeBuilder<Subscription> builder)
    {
        builder.ToTable("subscriptions");
        builder.HasKey(s => s.Id);
        builder.Property(s => s.Tier).IsRequired();
        builder.Property(s => s.StartsAt).IsRequired();
        builder.Property(s => s.EndsAt).IsRequired();
        builder.Property(s => s.StripeSubscriptionId).HasMaxLength(200);
        builder.Ignore(s => s.IsActive);
        builder.HasIndex(s => s.UserId);
    }
}
