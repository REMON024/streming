using StreamingPlatform.Domain.Enums;

namespace StreamingPlatform.Application.Common.Interfaces;

public interface ITokenService
{
    string GenerateAccessToken(Guid userId, string email, string name, Guid? profileId, SubscriptionTier tier, bool isAdmin);
    string GenerateRefreshToken();
    bool ValidateRefreshToken(string token);
}
