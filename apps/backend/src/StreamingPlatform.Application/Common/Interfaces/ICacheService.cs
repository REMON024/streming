namespace StreamingPlatform.Application.Common.Interfaces;

public interface ICacheService
{
    Task<T?> GetAsync<T>(string key, CancellationToken cancellationToken = default) where T : class;
    Task SetAsync<T>(string key, T value, TimeSpan? expiry = null, CancellationToken cancellationToken = default) where T : class;
    Task RemoveAsync(string key, CancellationToken cancellationToken = default);
    Task SetStringAsync(string key, string value, TimeSpan? expiry = null, CancellationToken cancellationToken = default);
    Task<string?> GetStringAsync(string key, CancellationToken cancellationToken = default);
}
