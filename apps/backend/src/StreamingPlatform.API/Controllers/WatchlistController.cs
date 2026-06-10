using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/watchlist")]
[Authorize]
public class WatchlistController(IApplicationDbContext db) : ControllerBase
{
    private Guid GetProfileId()
    {
        var profileIdStr = User.FindFirstValue("profileId");
        if (profileIdStr is null || !Guid.TryParse(profileIdStr, out var profileId))
            throw new UnauthorizedAccessException("No profile selected");
        return profileId;
    }

    [HttpGet]
    public async Task<IActionResult> GetWatchlist(CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var items = await db.WatchlistItems
            .Where(w => w.ProfileId == profileId)
            .Include(w => w.Content)
            .OrderByDescending(w => w.AddedAt)
            .Select(w => new ContentSummaryDto
            {
                Id = w.Content.Id,
                Title = w.Content.Title,
                Slug = w.Content.Slug,
                ThumbnailUrl = w.Content.ThumbnailUrl,
                BackdropUrl = w.Content.BackdropUrl,
                Type = w.Content.Type,
                ReleaseYear = w.Content.ReleaseYear,
                DurationMinutes = w.Content.DurationMinutes,
                RequiredTier = w.Content.RequiredTier,
                AverageRating = w.Content.AverageRating,
                IsFeatured = w.Content.IsFeatured,
                IsTrending = w.Content.IsTrending
            })
            .ToListAsync(cancellationToken);

        return Ok(items);
    }

    [HttpPost("{contentId:guid}")]
    public async Task<IActionResult> AddToWatchlist(Guid contentId, CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var content = await db.Contents.FindAsync([contentId], cancellationToken);
        if (content is null)
            return NotFound();

        var exists = await db.WatchlistItems
            .AnyAsync(w => w.ProfileId == profileId && w.ContentId == contentId, cancellationToken);

        if (exists)
            return Ok(new { message = "Already in watchlist" });

        var item = new WatchlistItem
        {
            ProfileId = profileId,
            ContentId = contentId,
            AddedAt = DateTimeOffset.UtcNow
        };
        db.WatchlistItems.Add(item);
        await db.SaveChangesAsync(cancellationToken);

        return Created($"/api/watchlist/{contentId}", null);
    }

    [HttpDelete("{contentId:guid}")]
    public async Task<IActionResult> RemoveFromWatchlist(Guid contentId, CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var item = await db.WatchlistItems
            .FirstOrDefaultAsync(w => w.ProfileId == profileId && w.ContentId == contentId, cancellationToken);

        if (item is null)
            return NotFound();

        db.WatchlistItems.Remove(item);
        await db.SaveChangesAsync(cancellationToken);

        return NoContent();
    }
}
