using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/channels")]
public class ChannelsController(IApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetAll(CancellationToken cancellationToken)
    {
        var channels = await db.Channels
            .Where(c => c.IsActive)
            .OrderBy(c => c.SortOrder)
            .Select(c => new ChannelDto
            {
                Id = c.Id,
                Name = c.Name,
                Slug = c.Slug,
                LogoUrl = c.LogoUrl,
                Category = c.Category,
                StreamUrl = string.Empty, // stream URL only returned on detail with auth check
                RequiredTier = c.RequiredTier
            })
            .ToListAsync(cancellationToken);

        return Ok(channels);
    }

    [HttpGet("{slug}")]
    [Authorize]
    public async Task<IActionResult> GetBySlug(string slug, CancellationToken cancellationToken)
    {
        var channel = await db.Channels
            .FirstOrDefaultAsync(c => c.Slug == slug && c.IsActive, cancellationToken);

        if (channel is null) return NotFound();

        var userTierClaim = User.FindFirstValue("tier");
        var userTier = userTierClaim is not null && int.TryParse(userTierClaim, out var t)
            ? (SubscriptionTier)t
            : SubscriptionTier.Free;

        if (userTier < channel.RequiredTier)
            return StatusCode(403, new { message = "Subscription tier insufficient to access this channel" });

        return Ok(new ChannelDto
        {
            Id = channel.Id,
            Name = channel.Name,
            Slug = channel.Slug,
            LogoUrl = channel.LogoUrl,
            Category = channel.Category,
            StreamUrl = channel.StreamUrl,
            RequiredTier = channel.RequiredTier
        });
    }
}
