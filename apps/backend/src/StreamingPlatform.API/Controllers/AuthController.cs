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
[Route("api/auth")]
public class AuthController(
    IApplicationDbContext db,
    ITokenService tokenService,
    ICacheService cacheService) : ControllerBase
{
    private static readonly TimeSpan RefreshTokenTtl = TimeSpan.FromDays(7);

    [HttpPost("register")]
    public async Task<ActionResult<LoginResponseDto>> Register(
        [FromBody] RegisterRequest request,
        CancellationToken cancellationToken)
    {
        if (await db.Users.AnyAsync(u => u.Email == request.Email, cancellationToken))
            return Conflict(new { message = "Email already in use" });

        var user = new User
        {
            Email = request.Email.ToLowerInvariant(),
            PasswordHash = BCrypt.Net.BCrypt.HashPassword(request.Password),
            Name = request.Name
        };

        db.Users.Add(user);

        // Create default profile
        var profile = new Profile
        {
            UserId = user.Id,
            Name = request.Name,
            IsKidsProfile = false
        };
        db.Profiles.Add(profile);

        // Create free subscription
        var subscription = new Subscription
        {
            UserId = user.Id,
            Tier = SubscriptionTier.Free,
            StartsAt = DateTimeOffset.UtcNow,
            EndsAt = DateTimeOffset.UtcNow.AddYears(100)
        };
        db.Subscriptions.Add(subscription);

        await db.SaveChangesAsync(cancellationToken);

        return Ok(await IssueTokens(user, profile.Id, SubscriptionTier.Free, cancellationToken));
    }

    [HttpPost("login")]
    public async Task<ActionResult<LoginResponseDto>> Login(
        [FromBody] LoginRequest request,
        CancellationToken cancellationToken)
    {
        var user = await db.Users
            .FirstOrDefaultAsync(u => u.Email == request.Email.ToLowerInvariant(), cancellationToken);

        if (user is null || !BCrypt.Net.BCrypt.Verify(request.Password, user.PasswordHash))
            return Unauthorized(new { message = "Invalid credentials" });

        var activeSub = await db.Subscriptions
            .Where(s => s.UserId == user.Id && s.EndsAt > DateTimeOffset.UtcNow)
            .OrderByDescending(s => s.Tier)
            .FirstOrDefaultAsync(cancellationToken);

        var tier = activeSub?.Tier ?? SubscriptionTier.Free;

        var profile = await db.Profiles
            .FirstOrDefaultAsync(p => p.UserId == user.Id, cancellationToken);

        return Ok(await IssueTokens(user, profile?.Id, tier, cancellationToken));
    }

    [HttpPost("refresh")]
    public async Task<ActionResult<LoginResponseDto>> Refresh(
        [FromBody] RefreshRequest request,
        CancellationToken cancellationToken)
    {
        var cacheKey = $"refresh:{request.RefreshToken}";
        var userIdStr = await cacheService.GetStringAsync(cacheKey, cancellationToken);

        if (userIdStr is null)
            return Unauthorized(new { message = "Invalid or expired refresh token" });

        if (!Guid.TryParse(userIdStr, out var userId))
            return Unauthorized(new { message = "Invalid token data" });

        var user = await db.Users.FindAsync([userId], cancellationToken);
        if (user is null)
            return Unauthorized(new { message = "User not found" });

        // Rotate refresh token
        await cacheService.RemoveAsync(cacheKey, cancellationToken);

        var activeSub = await db.Subscriptions
            .Where(s => s.UserId == user.Id && s.EndsAt > DateTimeOffset.UtcNow)
            .OrderByDescending(s => s.Tier)
            .FirstOrDefaultAsync(cancellationToken);

        var tier = activeSub?.Tier ?? SubscriptionTier.Free;

        var profile = await db.Profiles
            .FirstOrDefaultAsync(p => p.UserId == user.Id, cancellationToken);

        return Ok(await IssueTokens(user, profile?.Id, tier, cancellationToken));
    }

    [HttpPost("logout")]
    [Authorize]
    public async Task<IActionResult> Logout(
        [FromBody] RefreshRequest request,
        CancellationToken cancellationToken)
    {
        var cacheKey = $"refresh:{request.RefreshToken}";
        await cacheService.RemoveAsync(cacheKey, cancellationToken);
        return NoContent();
    }

    private async Task<LoginResponseDto> IssueTokens(User user, Guid? profileId, SubscriptionTier tier, CancellationToken cancellationToken)
    {
        var accessToken = tokenService.GenerateAccessToken(user.Id, user.Email, user.Name, profileId, tier, user.IsAdmin);
        var refreshToken = tokenService.GenerateRefreshToken();
        var refreshKey = $"refresh:{refreshToken}";
        await cacheService.SetStringAsync(refreshKey, user.Id.ToString(), RefreshTokenTtl, cancellationToken);

        return new LoginResponseDto
        {
            AccessToken = accessToken,
            RefreshToken = refreshToken,
            User = new UserDto
            {
                Id = user.Id,
                Email = user.Email,
                Name = user.Name,
                IsAdmin = user.IsAdmin
            }
        };
    }
}

public record RegisterRequest(string Email, string Password, string Name);
public record LoginRequest(string Email, string Password);
public record RefreshRequest(string RefreshToken);
