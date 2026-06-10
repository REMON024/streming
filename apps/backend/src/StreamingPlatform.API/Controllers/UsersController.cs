using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Entities;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.API.Controllers;

[ApiController]
[Route("api/users")]
[Authorize]
public class UsersController(
    IApplicationDbContext db,
    ITokenService tokenService) : ControllerBase
{
    private Guid GetUserId()
    {
        var sub = User.FindFirstValue(ClaimTypes.NameIdentifier)
                  ?? User.FindFirstValue("sub");
        if (sub is null || !Guid.TryParse(sub, out var userId))
            throw new UnauthorizedAccessException("Invalid user token");
        return userId;
    }

    [HttpGet("me")]
    public async Task<IActionResult> GetMe(CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var user = await db.Users.FindAsync([userId], cancellationToken);
        if (user is null) return NotFound();

        return Ok(new UserDto
        {
            Id = user.Id,
            Email = user.Email,
            Name = user.Name,
            IsAdmin = user.IsAdmin
        });
    }

    [HttpPut("me")]
    public async Task<IActionResult> UpdateMe(
        [FromBody] UpdateUserRequest request,
        CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var user = await db.Users.FindAsync([userId], cancellationToken);
        if (user is null) return NotFound();

        user.Name = request.Name;
        await db.SaveChangesAsync(cancellationToken);

        return Ok(new UserDto
        {
            Id = user.Id,
            Email = user.Email,
            Name = user.Name,
            IsAdmin = user.IsAdmin
        });
    }

    [HttpGet("me/profiles")]
    public async Task<IActionResult> GetProfiles(CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var profiles = await db.Profiles
            .Where(p => p.UserId == userId)
            .Select(p => new ProfileDto
            {
                Id = p.Id,
                Name = p.Name,
                AvatarUrl = p.AvatarUrl,
                IsKidsProfile = p.IsKidsProfile
            })
            .ToListAsync(cancellationToken);

        return Ok(profiles);
    }

    [HttpPost("me/profiles")]
    public async Task<IActionResult> CreateProfile(
        [FromBody] CreateProfileRequest request,
        CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var count = await db.Profiles.CountAsync(p => p.UserId == userId, cancellationToken);
        if (count >= 5)
            return BadRequest(new { message = "Maximum 5 profiles allowed per account" });

        var profile = new Profile
        {
            UserId = userId,
            Name = request.Name,
            AvatarUrl = request.AvatarUrl,
            IsKidsProfile = request.IsKidsProfile,
            PinHash = request.Pin is not null ? BCrypt.Net.BCrypt.HashPassword(request.Pin) : null
        };

        db.Profiles.Add(profile);
        await db.SaveChangesAsync(cancellationToken);

        return Created($"/api/users/me/profiles/{profile.Id}", new ProfileDto
        {
            Id = profile.Id,
            Name = profile.Name,
            AvatarUrl = profile.AvatarUrl,
            IsKidsProfile = profile.IsKidsProfile
        });
    }

    [HttpPut("me/profiles/{id:guid}")]
    public async Task<IActionResult> UpdateProfile(
        Guid id,
        [FromBody] UpdateProfileRequest request,
        CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var profile = await db.Profiles
            .FirstOrDefaultAsync(p => p.Id == id && p.UserId == userId, cancellationToken);

        if (profile is null) return NotFound();

        profile.Name = request.Name ?? profile.Name;
        profile.AvatarUrl = request.AvatarUrl ?? profile.AvatarUrl;
        profile.IsKidsProfile = request.IsKidsProfile ?? profile.IsKidsProfile;

        if (request.Pin is not null)
            profile.PinHash = BCrypt.Net.BCrypt.HashPassword(request.Pin);

        await db.SaveChangesAsync(cancellationToken);

        return Ok(new ProfileDto
        {
            Id = profile.Id,
            Name = profile.Name,
            AvatarUrl = profile.AvatarUrl,
            IsKidsProfile = profile.IsKidsProfile
        });
    }

    [HttpDelete("me/profiles/{id:guid}")]
    public async Task<IActionResult> DeleteProfile(Guid id, CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var profile = await db.Profiles
            .FirstOrDefaultAsync(p => p.Id == id && p.UserId == userId, cancellationToken);

        if (profile is null) return NotFound();

        var count = await db.Profiles.CountAsync(p => p.UserId == userId, cancellationToken);
        if (count <= 1)
            return BadRequest(new { message = "Cannot delete the last profile" });

        db.Profiles.Remove(profile);
        await db.SaveChangesAsync(cancellationToken);

        return NoContent();
    }

    [HttpPost("me/profiles/{id:guid}/select")]
    public async Task<IActionResult> SelectProfile(
        Guid id,
        [FromBody] SelectProfileRequest? request,
        CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var profile = await db.Profiles
            .FirstOrDefaultAsync(p => p.Id == id && p.UserId == userId, cancellationToken);

        if (profile is null) return NotFound();

        if (profile.PinHash is not null)
        {
            if (request?.Pin is null || !BCrypt.Net.BCrypt.Verify(request.Pin, profile.PinHash))
                return Unauthorized(new { message = "Invalid PIN" });
        }

        var user = await db.Users.FindAsync([userId], cancellationToken);
        if (user is null) return NotFound();

        var activeSub = await db.Subscriptions
            .Where(s => s.UserId == userId && s.EndsAt > DateTimeOffset.UtcNow)
            .OrderByDescending(s => s.Tier)
            .FirstOrDefaultAsync(cancellationToken);

        var tier = activeSub?.Tier ?? SubscriptionTier.Free;
        var newToken = tokenService.GenerateAccessToken(userId, user.Email, user.Name, id, tier, user.IsAdmin);

        return Ok(new { accessToken = newToken, profile = new ProfileDto
        {
            Id = profile.Id,
            Name = profile.Name,
            AvatarUrl = profile.AvatarUrl,
            IsKidsProfile = profile.IsKidsProfile
        }});
    }

    [HttpGet("me/subscription")]
    public async Task<IActionResult> GetSubscription(CancellationToken cancellationToken)
    {
        var userId = GetUserId();
        var sub = await db.Subscriptions
            .Where(s => s.UserId == userId && s.EndsAt > DateTimeOffset.UtcNow)
            .OrderByDescending(s => s.Tier)
            .FirstOrDefaultAsync(cancellationToken);

        if (sub is null)
            return Ok(new SubscriptionDto
            {
                Tier = SubscriptionTier.Free,
                StartsAt = DateTimeOffset.UtcNow,
                EndsAt = DateTimeOffset.MaxValue,
                IsActive = true
            });

        return Ok(new SubscriptionDto
        {
            Id = sub.Id,
            Tier = sub.Tier,
            StartsAt = sub.StartsAt,
            EndsAt = sub.EndsAt,
            IsActive = sub.IsActive,
            StripeSubscriptionId = sub.StripeSubscriptionId
        });
    }
}

public record UpdateUserRequest(string Name);
public record CreateProfileRequest(string Name, string? AvatarUrl, bool IsKidsProfile, string? Pin);
public record UpdateProfileRequest(string? Name, string? AvatarUrl, bool? IsKidsProfile, string? Pin);
public record SelectProfileRequest(string? Pin);
