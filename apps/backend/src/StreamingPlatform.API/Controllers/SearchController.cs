using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/search")]
public class SearchController(IApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Search(
        [FromQuery] string q,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(q))
            return BadRequest(new { message = "Query parameter 'q' is required" });

        var results = await db.Contents
            .FromSqlRaw(
                @"SELECT * FROM content
                  WHERE is_published = true
                    AND (similarity(title, {0}) > 0.2 OR search_vector @@ plainto_tsquery('english', {0}))
                  ORDER BY similarity(title, {0}) DESC, average_rating DESC
                  LIMIT {1} OFFSET {2}",
                q, pageSize, (page - 1) * pageSize)
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

        return Ok(new { items = results, page, pageSize, query = q });
    }
}
