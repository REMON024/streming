namespace StreamingPlatform.Application.Common.DTOs;

public class StreamInfoDto
{
    public string MasterM3u8Url { get; set; } = string.Empty;
    public string[] Qualities { get; set; } = Array.Empty<string>();
    public SubtitleDto[] Subtitles { get; set; } = Array.Empty<SubtitleDto>();
}
