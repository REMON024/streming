namespace StreamingPlatform.Application.Common.Interfaces;

public interface IStorageService
{
    Task<string> GetPresignedUploadUrlAsync(string bucket, string key, TimeSpan expiry, CancellationToken cancellationToken = default);
    Task<string> GetPresignedDownloadUrlAsync(string bucket, string key, TimeSpan expiry, CancellationToken cancellationToken = default);
}
