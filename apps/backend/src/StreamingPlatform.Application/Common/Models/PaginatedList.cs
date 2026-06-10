namespace StreamingPlatform.Application.Common.Models;

public class PaginatedList<T>
{
    public IReadOnlyList<T> Items { get; }
    public int TotalCount { get; }
    public int Page { get; }
    public int PageSize { get; }
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasNext => Page < TotalPages;
    public bool HasPrevious => Page > 1;

    public PaginatedList(IReadOnlyList<T> items, int totalCount, int page, int pageSize)
    {
        Items = items;
        TotalCount = totalCount;
        Page = page;
        PageSize = pageSize;
    }

    public static async Task<PaginatedList<T>> CreateAsync(
        IQueryable<T> source,
        int page,
        int pageSize,
        CancellationToken cancellationToken = default)
    {
        var count = source.Count();
        var items = source.Skip((page - 1) * pageSize).Take(pageSize).ToList();
        return new PaginatedList<T>(items, count, page, pageSize);
    }
}
