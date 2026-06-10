using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.Infrastructure.Persistence.Configurations;

public class WatchlistItemConfiguration : IEntityTypeConfiguration<WatchlistItem>
{
    public void Configure(EntityTypeBuilder<WatchlistItem> builder)
    {
        builder.ToTable("watchlist_items");
        builder.HasKey(w => w.Id);
        builder.HasIndex(w => new { w.ProfileId, w.ContentId }).IsUnique();
        builder.HasIndex(w => w.ProfileId);
    }
}
