namespace MatchEngine.Api.Models
{
    public record GetMatchesResponse(
        IReadOnlyList<MatchDetail> Matches
    );

    public record MatchDetail(
        string JobId,
        string JobTitle,
        float Score,
        string MatchLevel,
        string Assessment,
        List<string> KeyGaps,
        List<string> Suggestions
    );
}
