using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Configuration;
using StreamingPlatform.Application.Common.DTOs;
using StreamingPlatform.Application.Common.Interfaces;

namespace StreamingPlatform.Infrastructure.Services;

public class StreamingServiceClient(HttpClient httpClient, IConfiguration configuration) : IStreamingService
{
    private readonly string _internalKey = configuration["StreamingService:InternalKey"] ?? string.Empty;
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };

    public async Task NotifyTranscodeAsync(Guid videoAssetId, string rawPath, Guid? contentId, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, "/internal/transcode")
        {
            Content = JsonContent.Create(new
            {
                videoAssetId,
                rawPath,
                contentId
            })
        };
        request.Headers.Add("X-Internal-Key", _internalKey);
        var response = await httpClient.SendAsync(request, cancellationToken);
        response.EnsureSuccessStatusCode();
    }

    public async Task<StreamInfoDto?> GetStreamInfoAsync(Guid contentId, CancellationToken cancellationToken = default)
    {
        var request = new HttpRequestMessage(HttpMethod.Get, $"/stream/{contentId}/info");
        request.Headers.Add("X-Internal-Key", _internalKey);
        var response = await httpClient.SendAsync(request, cancellationToken);

        if (!response.IsSuccessStatusCode)
            return null;

        var json = await response.Content.ReadAsStringAsync(cancellationToken);
        return JsonSerializer.Deserialize<StreamInfoDto>(json, JsonOptions);
    }
}
