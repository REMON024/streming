using StreamingPlatform.Application.Common.DTOs;

namespace StreamingPlatform.Application.Common.Interfaces;

public interface IStreamingService
{
    Task NotifyTranscodeAsync(Guid videoAssetId, string rawPath, Guid? contentId, CancellationToken cancellationToken = default);
    Task<StreamInfoDto?> GetStreamInfoAsync(Guid contentId, CancellationToken cancellationToken = default);
}
