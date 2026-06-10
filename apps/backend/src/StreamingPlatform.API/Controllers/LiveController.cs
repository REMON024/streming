using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/live")]
public class LiveController(IApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll(CancellationToken cancellationToken)
    {
        var events = await db.LiveEvents
            .Where(e => e.Status == LiveStreamStatus.Scheduled || e.Status == LiveStreamStatus.Live)
            .OrderBy(e => e.StartTime)
            .Select(e => new LiveEventDto
            {
                Id = e.Id,
                Title = e.Title,
                ThumbnailUrl = e.ThumbnailUrl,
                SportType = e.SportType,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                Status = e.Status,
                RequiredTier = e.RequiredTier,
                IsFeatured = e.IsFeatured,
                StreamUrl = e.Status == LiveStreamStatus.Live ? e.HlsManifestPath : null
            })
            .ToListAsync(cancellationToken);

        return Ok(events);
    }

    [HttpGet("sports")]
    public async Task<IActionResult> GetSports(CancellationToken cancellationToken)
    {
        var events = await db.LiveEvents
            .Where(e =>
                e.SportType != null &&
                (e.Status == LiveStreamStatus.Scheduled || e.Status == LiveStreamStatus.Live))
            .OrderBy(e => e.StartTime)
            .Select(e => new LiveEventDto
            {
                Id = e.Id,
                Title = e.Title,
                ThumbnailUrl = e.ThumbnailUrl,
                SportType = e.SportType,
                StartTime = e.StartTime,
                EndTime = e.EndTime,
                Status = e.Status,
                RequiredTier = e.RequiredTier,
                IsFeatured = e.IsFeatured,
                StreamUrl = e.Status == LiveStreamStatus.Live ? e.HlsManifestPath : null
            })
            .ToListAsync(cancellationToken);

        return Ok(events);
    }

    [HttpGet("{id:guid}")]
    [Authorize]
    public async Task<IActionResult> GetById(Guid id, CancellationToken cancellationToken)
    {
        var liveEvent = await db.LiveEvents.FindAsync([id], cancellationToken);
        if (liveEvent is null) return NotFound();

        var userTierClaim = User.FindFirstValue("tier");
        var userTier = userTierClaim is not null && int.TryParse(userTierClaim, out var t)
            ? (SubscriptionTier)t
            : SubscriptionTier.Free;

        if (userTier < liveEvent.RequiredTier)
            return StatusCode(403, new { message = "Subscription tier insufficient" });

        return Ok(new LiveEventDto
        {
            Id = liveEvent.Id,
            Title = liveEvent.Title,
            ThumbnailUrl = liveEvent.ThumbnailUrl,
            SportType = liveEvent.SportType,
            StartTime = liveEvent.StartTime,
            EndTime = liveEvent.EndTime,
            Status = liveEvent.Status,
            RequiredTier = liveEvent.RequiredTier,
            IsFeatured = liveEvent.IsFeatured,
            StreamUrl = liveEvent.Status == LiveStreamStatus.Live ? liveEvent.HlsManifestPath : null
        });
    }
}
