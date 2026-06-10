using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/content")]
public class ContentController(
    IApplicationDbContext db,
    ICacheService cacheService,
    IStorageService storageService,
    IStreamingService streamingService,
    IConfiguration configuration) : ControllerBase
{
    private readonly int _cacheTtlMinutes = int.TryParse(configuration["Redis:CacheTtlMinutes"], out var m) ? m : 10;

    [HttpGet]
    public async Task<IActionResult> GetAll(
        [FromQuery] ContentType? type,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var query = db.Contents
            .Where(c => c.IsPublished)
            .AsQueryable();

        if (type.HasValue)
            query = query.Where(c => c.Type == type.Value);

        var total = await query.CountAsync(cancellationToken);
        var items = await query
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

        return Ok(new { items, total, page, pageSize, totalPages = (int)Math.Ceiling(total / (double)pageSize) });
    }

    [HttpGet("featured")]
    public async Task<IActionResult> GetFeatured(CancellationToken cancellationToken)
    {
        const string cacheKey = "content:featured";
        var cached = await cacheService.GetAsync<List<ContentSummaryDto>>(cacheKey, cancellationToken);
        if (cached is not null)
            return Ok(cached);

        var featured = await db.Contents
            .Where(c => c.IsPublished && c.IsFeatured)
            .OrderByDescending(c => c.AverageRating)
            .Take(20)
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

        await cacheService.SetAsync(cacheKey, featured, TimeSpan.FromMinutes(_cacheTtlMinutes), cancellationToken);
        return Ok(featured);
    }

    [HttpGet("trending")]
    public async Task<IActionResult> GetTrending(CancellationToken cancellationToken)
    {
        const string cacheKey = "content:trending";
        var cached = await cacheService.GetAsync<List<ContentSummaryDto>>(cacheKey, cancellationToken);
        if (cached is not null)
            return Ok(cached);

        var trending = await db.Contents
            .Where(c => c.IsPublished && c.IsTrending)
            .OrderByDescending(c => c.AverageRating)
            .Take(20)
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

        await cacheService.SetAsync(cacheKey, trending, TimeSpan.FromMinutes(_cacheTtlMinutes), cancellationToken);
        return Ok(trending);
    }

    [HttpGet("genres")]
    public async Task<IActionResult> GetGenres(CancellationToken cancellationToken)
    {
        var genres = await db.Genres
            .OrderBy(g => g.Name)
            .Select(g => new GenreDto { Id = g.Id, Name = g.Name, Slug = g.Slug })
            .ToListAsync(cancellationToken);
        return Ok(genres);
    }

    [HttpGet("genre/{slug}")]
    public async Task<IActionResult> GetByGenre(
        string slug,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var genre = await db.Genres.FirstOrDefaultAsync(g => g.Slug == slug, cancellationToken);
        if (genre is null)
            return NotFound();

        var query = db.ContentGenres
            .Where(cg => cg.GenreId == genre.Id && cg.Content.IsPublished)
            .Select(cg => cg.Content);

        var total = await query.CountAsync(cancellationToken);
        var items = await query
            .OrderByDescending(c => c.AverageRating)
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

        return Ok(new { items, total, page, pageSize, totalPages = (int)Math.Ceiling(total / (double)pageSize) });
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id, CancellationToken cancellationToken)
    {
        var content = await db.Contents
            .Include(c => c.ContentGenres).ThenInclude(cg => cg.Genre)
            .Include(c => c.Seasons).ThenInclude(s => s.Episodes).ThenInclude(e => e.VideoAssets)
            .Include(c => c.Seasons).ThenInclude(s => s.Episodes).ThenInclude(e => e.Subtitles)
            .Include(c => c.VideoAssets)
            .Include(c => c.Subtitles)
            .FirstOrDefaultAsync(c => c.Id == id && c.IsPublished, cancellationToken);

        if (content is null)
            return NotFound();

        var dto = new ContentDetailDto
        {
            Id = content.Id,
            Title = content.Title,
            Slug = content.Slug,
            Description = content.Description,
            ThumbnailUrl = content.ThumbnailUrl,
            BackdropUrl = content.BackdropUrl,
            Type = content.Type,
            ReleaseYear = content.ReleaseYear,
            DurationMinutes = content.DurationMinutes,
            RequiredTier = content.RequiredTier,
            AverageRating = content.AverageRating,
            IsFeatured = content.IsFeatured,
            IsTrending = content.IsTrending,
            Genres = content.ContentGenres.Select(cg => new GenreDto
            {
                Id = cg.Genre.Id,
                Name = cg.Genre.Name,
                Slug = cg.Genre.Slug
            }).ToList(),
            Seasons = content.Seasons.OrderBy(s => s.SeasonNumber).Select(s => new SeasonDto
            {
                Id = s.Id,
                SeasonNumber = s.SeasonNumber,
                Title = s.Title,
                Description = s.Description,
                Episodes = s.Episodes.OrderBy(e => e.EpisodeNumber).Select(e => new EpisodeDto
                {
                    Id = e.Id,
                    EpisodeNumber = e.EpisodeNumber,
                    Title = e.Title,
                    Description = e.Description,
                    DurationMinutes = e.DurationMinutes,
                    ThumbnailUrl = e.ThumbnailUrl,
                    VideoAssets = e.VideoAssets.Select(v => new VideoAssetDto
                    {
                        Id = v.Id,
                        Quality = v.Quality,
                        HlsManifestPath = v.HlsManifestPath,
                        Status = v.Status,
                        FileSizeBytes = v.FileSizeBytes,
                        BitrateKbps = v.BitrateKbps
                    }).ToList(),
                    Subtitles = e.Subtitles.Select(sub => new SubtitleDto
                    {
                        LanguageCode = sub.LanguageCode,
                        LanguageName = sub.LanguageName,
                        FileUrl = sub.FileUrl
                    }).ToList()
                }).ToList()
            }).ToList(),
            VideoAssets = content.VideoAssets.Select(v => new VideoAssetDto
            {
                Id = v.Id,
                Quality = v.Quality,
                HlsManifestPath = v.HlsManifestPath,
                Status = v.Status,
                FileSizeBytes = v.FileSizeBytes,
                BitrateKbps = v.BitrateKbps
            }).ToList(),
            Subtitles = content.Subtitles.Select(s => new SubtitleDto
            {
                LanguageCode = s.LanguageCode,
                LanguageName = s.LanguageName,
                FileUrl = s.FileUrl
            }).ToList()
        };

        return Ok(dto);
    }

    [HttpGet("{id:guid}/stream")]
    [Authorize]
    public async Task<IActionResult> GetStream(Guid id, CancellationToken cancellationToken)
    {
        var content = await db.Contents
            .FirstOrDefaultAsync(c => c.Id == id && c.IsPublished, cancellationToken);

        if (content is null)
            return NotFound();

        var userTierClaim = User.FindFirstValue("tier");
        var userTier = userTierClaim is not null && int.TryParse(userTierClaim, out var t)
            ? (SubscriptionTier)t
            : SubscriptionTier.Free;

        if (userTier < content.RequiredTier)
            return StatusCode(403, new { message = "Subscription tier insufficient" });

        var streamInfo = await streamingService.GetStreamInfoAsync(id, cancellationToken);
        if (streamInfo is null)
            return StatusCode(503, new { message = "Streaming service unavailable" });

        return Ok(streamInfo);
    }

    [HttpPost("{id:guid}/upload")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> GetUploadUrl(
        Guid id,
        [FromBody] UploadRequest request,
        CancellationToken cancellationToken)
    {
        var content = await db.Contents.FindAsync([id], cancellationToken);
        if (content is null)
            return NotFound();

        var bucket = configuration["Minio:BucketVideosRaw"] ?? "videos-raw";
        var key = $"{id}/{Guid.NewGuid()}{Path.GetExtension(request.FileName)}";
        var url = await storageService.GetPresignedUploadUrlAsync(bucket, key, TimeSpan.FromHours(2), cancellationToken);

        return Ok(new { uploadUrl = url, key });
    }
}

public record UploadRequest(string FileName);
