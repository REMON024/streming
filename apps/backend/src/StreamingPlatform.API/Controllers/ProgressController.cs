using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Entities;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/progress")]
[Authorize]
public class ProgressController(IApplicationDbContext db) : ControllerBase
{
    private Guid GetProfileId()
    {
        var profileIdStr = User.FindFirstValue("profileId");
        if (profileIdStr is null || !Guid.TryParse(profileIdStr, out var profileId))
            throw new UnauthorizedAccessException("No profile selected");
        return profileId;
    }

    [HttpGet]
    public async Task<IActionResult> GetProgress(CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var progresses = await db.WatchProgresses
            .Where(w => w.ProfileId == profileId)
            .OrderByDescending(w => w.LastWatchedAt)
            .Take(20)
            .Select(w => new WatchProgressDto
            {
                ContentId = w.ContentId,
                EpisodeId = w.EpisodeId,
                PositionSeconds = w.PositionSeconds,
                TotalDurationSeconds = w.TotalDurationSeconds,
                IsCompleted = w.IsCompleted,
                LastWatchedAt = w.LastWatchedAt
            })
            .ToListAsync(cancellationToken);

        return Ok(progresses);
    }

    [HttpGet("{contentId:guid}")]
    public async Task<IActionResult> GetProgressForContent(Guid contentId, CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var progress = await db.WatchProgresses
            .Where(w => w.ProfileId == profileId && w.ContentId == contentId)
            .OrderByDescending(w => w.LastWatchedAt)
            .Select(w => new WatchProgressDto
            {
                ContentId = w.ContentId,
                EpisodeId = w.EpisodeId,
                PositionSeconds = w.PositionSeconds,
                TotalDurationSeconds = w.TotalDurationSeconds,
                IsCompleted = w.IsCompleted,
                LastWatchedAt = w.LastWatchedAt
            })
            .FirstOrDefaultAsync(cancellationToken);

        if (progress is null)
            return NotFound();

        return Ok(progress);
    }

    [HttpPut("{contentId:guid}")]
    public async Task<IActionResult> UpsertProgress(
        Guid contentId,
        [FromBody] UpsertProgressRequest request,
        CancellationToken cancellationToken)
    {
        var profileId = GetProfileId();

        var existing = await db.WatchProgresses
            .FirstOrDefaultAsync(w =>
                w.ProfileId == profileId &&
                w.ContentId == contentId &&
                w.EpisodeId == request.EpisodeId,
                cancellationToken);

        var isCompleted = request.TotalDurationSeconds > 0 &&
                          request.PositionSeconds >= request.TotalDurationSeconds * 0.9;

        if (existing is null)
        {
            var progress = new WatchProgress
            {
                ProfileId = profileId,
                ContentId = contentId,
                EpisodeId = request.EpisodeId,
                PositionSeconds = request.PositionSeconds,
                TotalDurationSeconds = request.TotalDurationSeconds,
                IsCompleted = isCompleted,
                LastWatchedAt = DateTimeOffset.UtcNow
            };
            db.WatchProgresses.Add(progress);
        }
        else
        {
            existing.PositionSeconds = request.PositionSeconds;
            existing.TotalDurationSeconds = request.TotalDurationSeconds;
            existing.IsCompleted = isCompleted;
            existing.LastWatchedAt = DateTimeOffset.UtcNow;
        }

        await db.SaveChangesAsync(cancellationToken);
        return NoContent();
    }
}

public record UpsertProgressRequest(Guid? EpisodeId, int PositionSeconds, int TotalDurationSeconds);
