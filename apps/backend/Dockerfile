FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["src/StreamingPlatform.API/StreamingPlatform.API.csproj", "src/StreamingPlatform.API/"]
COPY ["src/StreamingPlatform.Application/StreamingPlatform.Application.csproj", "src/StreamingPlatform.Application/"]
COPY ["src/StreamingPlatform.Domain/StreamingPlatform.Domain.csproj", "src/StreamingPlatform.Domain/"]
COPY ["src/StreamingPlatform.Infrastructure/StreamingPlatform.Infrastructure.csproj", "src/StreamingPlatform.Infrastructure/"]
RUN dotnet restore "src/StreamingPlatform.API/StreamingPlatform.API.csproj"
COPY . .
RUN dotnet publish "src/StreamingPlatform.API/StreamingPlatform.API.csproj" -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "StreamingPlatform.API.dll"]
