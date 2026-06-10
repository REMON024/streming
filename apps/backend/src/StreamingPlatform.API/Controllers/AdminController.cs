using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Entities;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/admin")]
[Authorize(Roles = "Admin")]
public class AdminController(
    IApplicationDbContext db,
    ICacheService cacheService,
    IConfiguration configuration) : ControllerBase
{
    // ==================== CONTENT CRUD ====================

    [HttpGet("content")]
    public async Task<IActionResult> GetAllContent(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var total = await db.Contents.CountAsync(cancellationToken);
        var items = await db.Contents
            .OrderByDescending(c => c.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(c => new ContentSummaryDto
            {
                Id = c.Id,
                Title = c.Title,
                Slug = c.Slug,
                ThumbnailUrl = c.ThumbnailUrl,
                BackdropUrl = c.BackdropUrl,
                Type = c.Type,
                ReleaseYear = c.ReleaseYear,
                DurationMinutes = c.DurationMinutes,
                RequiredTier = c.RequiredTier,
                AverageRating = c.AverageRating,
                IsFeatured = c.IsFeatured,
                IsTrending = c.IsTrending
            })
            .ToListAsync(cancellationToken);

        return Ok(new { items, total, page, pageSize });
    }

    [HttpPost("content")]
    public async Task<IActionResult> CreateContent(
        [FromBody] CreateContentRequest request,
        CancellationToken cancellationToken)
    {
        var content = new Content
        {
            Title = request.Title,
            Slug = request.Slug,
            Description = request.Description,
            ThumbnailUrl = request.ThumbnailUrl,
            BackdropUrl = request.BackdropUrl,
            ReleaseYear = request.ReleaseYear,
            DurationMinutes = request.DurationMinutes,
            Type = request.Type,
            RequiredTier = request.RequiredTier,
            IsPublished = request.IsPublished,
            IsFeatured = request.IsFeatured,
            IsTrending = request.IsTrending
        };

        db.Contents.Add(content);

        if (request.GenreIds?.Any() == true)
        {
            foreach (var genreId in request.GenreIds)
            {
                db.ContentGenres.Add(new ContentGenre { ContentId = content.Id, GenreId = genreId });
            }
        }

        await db.SaveChangesAsync(cancellationToken);
        await InvalidateContentCache(cancellationToken);

        return Created($"/api/content/{content.Id}", new { id = content.Id });
    }

    [HttpPut("content/{id:guid}")]
    public async Task<IActionResult> UpdateContent(
        Guid id,
        [FromBody] UpdateContentRequest request,
        CancellationToken cancellationToken)
    {
        var content = await db.Contents.FindAsync([id], cancellationToken);
        if (content is null) return NotFound();

        content.Title = request.Title ?? content.Title;
        content.Slug = request.Slug ?? content.Slug;
        content.Description = request.Description ?? content.Description;
        content.ThumbnailUrl = request.ThumbnailUrl ?? content.ThumbnailUrl;
        content.BackdropUrl = request.BackdropUrl ?? content.BackdropUrl;
        content.ReleaseYear = request.ReleaseYear ?? content.ReleaseYear;
        content.DurationMinutes = request.DurationMinutes ?? content.DurationMinutes;
        content.Type = request.Type ?? content.Type;
        content.RequiredTier = request.RequiredTier ?? content.RequiredTier;
        content.IsPublished = request.IsPublished ?? content.IsPublished;
        content.IsFeatured = request.IsFeatured ?? content.IsFeatured;
        content.IsTrending = request.IsTrending ?? content.IsTrending;

        await db.SaveChangesAsync(cancellationToken);
        await InvalidateContentCache(cancellationToken);

        return NoContent();
    }

    [HttpDelete("content/{id:guid}")]
    public async Task<IActionResult> DeleteContent(Guid id, CancellationToken cancellationToken)
    {
        var content = await db.Contents.FindAsync([id], cancellationToken);
        if (content is null) return NotFound();

        db.Contents.Remove(content);
        await db.SaveChangesAsync(cancellationToken);
        await InvalidateContentCache(cancellationToken);

        return NoContent();
    }

    // ==================== CHANNELS CRUD ====================

    [HttpGet("channels")]
    public async Task<IActionResult> GetAllChannels(CancellationToken cancellationToken)
    {
        var channels = await db.Channels
            .OrderBy(c => c.SortOrder)
            .Select(c => new ChannelDto
            {
                Id = c.Id,
                Name = c.Name,
                Slug = c.Slug,
                LogoUrl = c.LogoUrl,
                Category = c.Category,
                StreamUrl = c.StreamUrl,
                RequiredTier = c.RequiredTier
            })
            .ToListAsync(cancellationToken);

        return Ok(channels);
    }

    [HttpPost("channels")]
    public async Task<IActionResult> CreateChannel(
        [FromBody] CreateChannelRequest request,
        CancellationToken cancellationToken)
    {
        var channel = new Channel
        {
            Name = request.Name,
            Slug = request.Slug,
            Description = request.Description,
            LogoUrl = request.LogoUrl,
            StreamUrl = request.StreamUrl,
            Category = request.Category,
            RequiredTier = request.RequiredTier,
            IsActive = request.IsActive,
            SortOrder = request.SortOrder
        };

        db.Channels.Add(channel);
        await db.SaveChangesAsync(cancellationToken);

        return Created($"/api/channels/{channel.Slug}", new { id = channel.Id });
    }

    [HttpPut("channels/{id:guid}")]
    public async Task<IActionResult> UpdateChannel(
        Guid id,
        [FromBody] UpdateChannelRequest request,
        CancellationToken cancellationToken)
    {
        var channel = await db.Channels.FindAsync([id], cancellationToken);
        if (channel is null) return NotFound();

        channel.Name = request.Name ?? channel.Name;
        channel.Slug = request.Slug ?? channel.Slug;
        channel.Description = request.Description ?? channel.Description;
        channel.LogoUrl = request.LogoUrl ?? channel.LogoUrl;
        channel.StreamUrl = request.StreamUrl ?? channel.StreamUrl;
        channel.Category = request.Category ?? channel.Category;
        channel.RequiredTier = request.RequiredTier ?? channel.RequiredTier;
        channel.IsActive = request.IsActive ?? channel.IsActive;
        channel.SortOrder = request.SortOrder ?? channel.SortOrder;

        await db.SaveChangesAsync(cancellationToken);
        return NoContent();
    }

    [HttpDelete("channels/{id:guid}")]
    public async Task<IActionResult> DeleteChannel(Guid id, CancellationToken cancellationToken)
    {
        var channel = await db.Channels.FindAsync([id], cancellationToken);
        if (channel is null) return NotFound();

        db.Channels.Remove(channel);
        await db.SaveChangesAsync(cancellationToken);
        return NoContent();
    }

    // ==================== LIVE EVENTS CRUD ====================

    [HttpGet("live-events")]
    public async Task<IActionResult> GetAllLiveEvents(CancellationToken cancellationToken)
    {
        var events = await db.LiveEvents
            .OrderByDescending(e => e.StartTime)
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
                StreamUrl = e.HlsManifestPath
            })
            .ToListAsync(cancellationToken);

        return Ok(events);
    }

    [HttpPost("live-events")]
    public async Task<IActionResult> CreateLiveEvent(
        [FromBody] CreateLiveEventRequest request,
        CancellationToken cancellationToken)
    {
        var liveEvent = new LiveEvent
        {
            Title = request.Title,
            Description = request.Description,
            ThumbnailUrl = request.ThumbnailUrl,
            SportType = request.SportType,
            StartTime = request.StartTime,
            EndTime = request.EndTime,
            Status = request.Status,
            HlsManifestPath = request.HlsManifestPath,
            RequiredTier = request.RequiredTier,
            IsFeatured = request.IsFeatured
        };

        db.LiveEvents.Add(liveEvent);
        await db.SaveChangesAsync(cancellationToken);

        return Created($"/api/live/{liveEvent.Id}", new { id = liveEvent.Id });
    }

    [HttpPut("live-events/{id:guid}")]
    public async Task<IActionResult> UpdateLiveEvent(
        Guid id,
        [FromBody] UpdateLiveEventRequest request,
        CancellationToken cancellationToken)
    {
        var liveEvent = await db.LiveEvents.FindAsync([id], cancellationToken);
        if (liveEvent is null) return NotFound();

        liveEvent.Title = request.Title ?? liveEvent.Title;
        liveEvent.Description = request.Description ?? liveEvent.Description;
        liveEvent.ThumbnailUrl = request.ThumbnailUrl ?? liveEvent.ThumbnailUrl;
        liveEvent.SportType = request.SportType ?? liveEvent.SportType;
        liveEvent.StartTime = request.StartTime ?? liveEvent.StartTime;
        liveEvent.EndTime = request.EndTime ?? liveEvent.EndTime;
        liveEvent.Status = request.Status ?? liveEvent.Status;
        liveEvent.HlsManifestPath = request.HlsManifestPath ?? liveEvent.HlsManifestPath;
        liveEvent.RequiredTier = request.RequiredTier ?? liveEvent.RequiredTier;
        liveEvent.IsFeatured = request.IsFeatured ?? liveEvent.IsFeatured;

        await db.SaveChangesAsync(cancellationToken);
        return NoContent();
    }

    [HttpDelete("live-events/{id:guid}")]
    public async Task<IActionResult> DeleteLiveEvent(Guid id, CancellationToken cancellationToken)
    {
        var liveEvent = await db.LiveEvents.FindAsync([id], cancellationToken);
        if (liveEvent is null) return NotFound();

        db.LiveEvents.Remove(liveEvent);
        await db.SaveChangesAsync(cancellationToken);
        return NoContent();
    }

    // ==================== ASSET CALLBACK ====================

    [HttpPatch("assets/{id:guid}/status")]
    [AllowAnonymous] // validated by header
    public async Task<IActionResult> UpdateAssetStatus(
        Guid id,
        [FromBody] UpdateAssetStatusRequest request,
        CancellationToken cancellationToken)
    {
        var internalKey = configuration["StreamingService:InternalKey"] ?? string.Empty;
        if (!Request.Headers.TryGetValue("X-Internal-Key", out var headerKey) || headerKey != internalKey)
            return Unauthorized(new { message = "Invalid internal key" });

        var asset = await db.VideoAssets.FindAsync([id], cancellationToken);
        if (asset is null) return NotFound();

        asset.Status = request.Status;
        asset.HlsManifestPath = request.HlsManifestPath ?? asset.HlsManifestPath;

        if (request.Status == ProcessingStatus.Ready)
            asset.ProcessedAt = DateTimeOffset.UtcNow;

        await db.SaveChangesAsync(cancellationToken);

        // Invalidate content cache if this asset belongs to content
        if (asset.ContentId.HasValue)
        {
            await cacheService.RemoveAsync($"content:{asset.ContentId}", cancellationToken);
            await InvalidateContentCache(cancellationToken);
        }

        return NoContent();
    }

    private async Task InvalidateContentCache(CancellationToken cancellationToken)
    {
        await cacheService.RemoveAsync("content:featured", cancellationToken);
        await cacheService.RemoveAsync("content:trending", cancellationToken);
    }
}

// Request models
public record CreateContentRequest(
    string Title,
    string Slug,
    string Description,
    string? ThumbnailUrl,
    string? BackdropUrl,
    int ReleaseYear,
    int DurationMinutes,
    ContentType Type,
    SubscriptionTier RequiredTier,
    bool IsPublished,
    bool IsFeatured,
    bool IsTrending,
    List<Guid>? GenreIds);

public record UpdateContentRequest(
    string? Title,
    string? Slug,
    string? Description,
    string? ThumbnailUrl,
    string? BackdropUrl,
    int? ReleaseYear,
    int? DurationMinutes,
    ContentType? Type,
    SubscriptionTier? RequiredTier,
    bool? IsPublished,
    bool? IsFeatured,
    bool? IsTrending);

public record CreateChannelRequest(
    string Name,
    string Slug,
    string? Description,
    string? LogoUrl,
    string StreamUrl,
    string Category,
    SubscriptionTier RequiredTier,
    bool IsActive,
    int SortOrder);

public record UpdateChannelRequest(
    string? Name,
    string? Slug,
    string? Description,
    string? LogoUrl,
    string? StreamUrl,
    string? Category,
    SubscriptionTier? RequiredTier,
    bool? IsActive,
    int? SortOrder);

public record CreateLiveEventRequest(
    string Title,
    string? Description,
    string? ThumbnailUrl,
    string? SportType,
    DateTimeOffset StartTime,
    DateTimeOffset? EndTime,
    LiveStreamStatus Status,
    string? HlsManifestPath,
    SubscriptionTier RequiredTier,
    bool IsFeatured);

public record UpdateLiveEventRequest(
    string? Title,
    string? Description,
    string? ThumbnailUrl,
    string? SportType,
    DateTimeOffset? StartTime,
    DateTimeOffset? EndTime,
    LiveStreamStatus? Status,
    string? HlsManifestPath,
    SubscriptionTier? RequiredTier,
    bool? IsFeatured);

public record UpdateAssetStatusRequest(ProcessingStatus Status, string? HlsManifestPath);
