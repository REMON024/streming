using Minio;
using Minio.DataModel.Args;
using StreamingPlatform.Application.Common.Interfaces;

namespace StreamingPlatform.Infrastructure.Services;

public class MinioStorageService(IMinioClient minioClient) : IStorageService
{
    public async Task<string> GetPresignedUploadUrlAsync(string bucket, string key, TimeSpan expiry, CancellationToken cancellationToken = default)
    {
        var args = new PresignedPutObjectArgs()
            .WithBucket(bucket)
            .WithObject(key)
            .WithExpiry((int)expiry.TotalSeconds);

        return await minioClient.PresignedPutObjectAsync(args);
    }

    public async Task<string> GetPresignedDownloadUrlAsync(string bucket, string key, TimeSpan expiry, CancellationToken cancellationToken = default)
    {
        var args = new PresignedGetObjectArgs()
            .WithBucket(bucket)
            .WithObject(key)
            .WithExpiry((int)expiry.TotalSeconds);

        return await minioClient.PresignedGetObjectAsync(args);
    }
}
