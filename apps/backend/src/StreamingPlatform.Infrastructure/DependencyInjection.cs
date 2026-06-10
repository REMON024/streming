using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Minio;
using StackExchange.Redis;
using StreamingPlatform.Application.Common.Interfaces;
using StreamingPlatform.Infrastructure.Persistence;
using StreamingPlatform.Infrastructure.Services;

namespace StreamingPlatform.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // EF Core with Npgsql
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseNpgsql(
                configuration.GetConnectionString("DefaultConnection"),
                npgsql => npgsql.MigrationsAssembly(typeof(ApplicationDbContext).Assembly.FullName)
            )
        );
        services.AddScoped<IApplicationDbContext>(provider => provider.GetRequiredService<ApplicationDbContext>());

        // Redis
        var redisConnectionString = configuration.GetConnectionString("Redis")
            ?? configuration["Redis:ConnectionString"]
            ?? "localhost:6379";
        services.AddSingleton<IConnectionMultiplexer>(_ =>
            ConnectionMultiplexer.Connect(redisConnectionString));

        // MinIO
        services.AddSingleton<IMinioClient>(_ =>
        {
            var endpoint = configuration["Minio:Endpoint"] ?? "localhost:9000";
            var accessKey = configuration["Minio:AccessKey"] ?? "minioadmin";
            var secretKey = configuration["Minio:SecretKey"] ?? "minioadmin";
            var useSSL = bool.TryParse(configuration["Minio:UseSSL"], out var ssl) && ssl;

            return new MinioClient()
                .WithEndpoint(endpoint)
                .WithCredentials(accessKey, secretKey)
                .WithSSL(useSSL)
                .Build();
        });

        // Streaming service HTTP client
        services.AddHttpClient<IStreamingService, StreamingServiceClient>(client =>
        {
            var streamingUrl = configuration["StreamingService:BaseUrl"] ?? "http://localhost:8080";
            client.BaseAddress = new Uri(streamingUrl);
            client.Timeout = TimeSpan.FromSeconds(30);
        });

        // Services
        services.AddScoped<ITokenService, TokenService>();
        services.AddScoped<ICacheService, CacheService>();
        services.AddScoped<IStorageService, MinioStorageService>();

        return services;
    }
}
