using System.Text.Json;
using StackExchange.Redis;
using StreamingPlatform.Application.Common.Interfaces;

namespace StreamingPlatform.Infrastructure.Services;

public class CacheService(IConnectionMultiplexer redis) : ICacheService
{
    private readonly IDatabase _db = redis.GetDatabase();
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public async Task<T?> GetAsync<T>(string key, CancellationToken cancellationToken = default) where T : class
    {
        var value = await _db.StringGetAsync(key);
        if (!value.HasValue)
            return null;
        return JsonSerializer.Deserialize<T>(value.ToString(), JsonOptions);
    }

    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null, CancellationToken cancellationToken = default) where T : class
    {
        var serialized = JsonSerializer.Serialize(value, JsonOptions);
        await _db.StringSetAsync(key, serialized, expiry);
    }

    public async Task RemoveAsync(string key, CancellationToken cancellationToken = default)
    {
        await _db.KeyDeleteAsync(key);
    }

    public async Task SetStringAsync(string key, string value, TimeSpan? expiry = null, CancellationToken cancellationToken = default)
    {
        await _db.StringSetAsync(key, value, expiry);
    }

    public async Task<string?> GetStringAsync(string key, CancellationToken cancellationToken = default)
    {
        var value = await _db.StringGetAsync(key);
        return value.HasValue ? value.ToString() : null;
    }
}
