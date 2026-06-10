using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Infrastructure.Services;

public class TokenService(IConfiguration configuration) : ITokenService
{
    private readonly string _secret = configuration["Jwt:Secret"]
        ?? throw new InvalidOperationException("Jwt:Secret is not configured");
    private readonly string _issuer = configuration["Jwt:Issuer"] ?? "streaming-platform";
    private readonly string _audience = configuration["Jwt:Audience"] ?? "streaming-platform-client";
    private readonly int _accessTokenMinutes = int.TryParse(configuration["Jwt:AccessTokenMinutes"], out var mins) ? mins : 15;

    public string GenerateAccessToken(Guid userId, string email, string name, Guid? profileId, SubscriptionTier tier, bool isAdmin)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secret));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, userId.ToString()),
            new(JwtRegisteredClaimNames.Email, email),
            new("name", name),
            new("tier", ((int)tier).ToString()),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new(JwtRegisteredClaimNames.Iat, DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString(), ClaimValueTypes.Integer64),
        };

        if (profileId.HasValue)
        {
            claims.Add(new Claim("profileId", profileId.Value.ToString()));
        }

        if (isAdmin)
        {
            claims.Add(new Claim(ClaimTypes.Role, "Admin"));
        }

        claims.Add(new Claim(ClaimTypes.Role, "User"));

        var token = new JwtSecurityToken(
            issuer: _issuer,
            audience: _audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_accessTokenMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    public string GenerateRefreshToken()
    {
        return Guid.NewGuid().ToString("N");
    }

    public bool ValidateRefreshToken(string token)
    {
        return !string.IsNullOrWhiteSpace(token) && token.Length == 32;
    }
}
