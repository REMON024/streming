using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;

namespace StreamingPlatform.API.Controllers;

// Bound from appsettings.json "Ads" section
public sealed class AdsSettings
{
    public bool Enabled { get; init; } = true;
    public int MidRollIntervalMinutes { get; init; } = 15;
    public PreRollSettings PreRoll { get; init; } = new();
    public MidRollSettings MidRoll { get; init; } = new();
}

public sealed class PreRollSettings
{
    public string VideoUrl { get; init; } = string.Empty;
    public string? ClickThroughUrl { get; init; }
    public string? AdvertiserName { get; init; }
    public int SkipAfterSeconds { get; init; } = 5;
}

public sealed class MidRollSettings
{
    public string ImageUrl { get; init; } = string.Empty;
    public string? ClickThroughUrl { get; init; }
    public string? AdvertiserName { get; init; }
    public string Headline { get; init; } = string.Empty;
    public int DurationSeconds { get; init; } = 30;
    public int CloseAfterSeconds { get; init; } = 5;
}

// Response DTO sent to the frontend
public sealed record AdsConfigResponse(
    bool Enabled,
    int MidRollIntervalSeconds,
    PreRollDto PreRoll,
    MidRollDto MidRoll
);

public sealed record PreRollDto(
    string VideoUrl,
    string? ClickThroughUrl,
    string? AdvertiserName,
    int SkipAfterSeconds
);

public sealed record MidRollDto(
    string ImageUrl,
    string? ClickThroughUrl,
    string? AdvertiserName,
    string Headline,
    int DurationSeconds,
    int CloseAfterSeconds
);

[ApiController]
[Route("api/ads")]
public class AdsController(IOptions<AdsSettings> options) : ControllerBase
{
    private readonly AdsSettings _settings = options.Value;

    /// <summary>
    /// Returns the current ad configuration for the player.
    /// Free-tier clients call this once on player mount to get live ad settings.
    /// No authentication required — ads must load even for unauthenticated sessions.
    /// </summary>
    [HttpGet("config")]
    [ResponseCache(Duration = 300)] // cache 5 minutes on CDN/browser
    public ActionResult<AdsConfigResponse> GetConfig()
    {
        var response = new AdsConfigResponse(
            Enabled: _settings.Enabled,
            MidRollIntervalSeconds: _settings.MidRollIntervalMinutes * 60,
            PreRoll: new PreRollDto(
                VideoUrl: _settings.PreRoll.VideoUrl,
                ClickThroughUrl: _settings.PreRoll.ClickThroughUrl,
                AdvertiserName: _settings.PreRoll.AdvertiserName,
                SkipAfterSeconds: _settings.PreRoll.SkipAfterSeconds
            ),
            MidRoll: new MidRollDto(
                ImageUrl: _settings.MidRoll.ImageUrl,
                ClickThroughUrl: _settings.MidRoll.ClickThroughUrl,
                AdvertiserName: _settings.MidRoll.AdvertiserName,
                Headline: _settings.MidRoll.Headline,
                DurationSeconds: _settings.MidRoll.DurationSeconds,
                CloseAfterSeconds: _settings.MidRoll.CloseAfterSeconds
            )
        );

        return Ok(response);
    }
}
