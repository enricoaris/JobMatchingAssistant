namespace MatchEngine.Api.Models;
public class UpdateInsightsRequest
{
    public string? MatchId { get; set; }
    public string? MatchLevel { get; set; }
    public List<string>? KeyGaps { get; set; }
    public string? Assessment { get; set; }
    public List<string>? Suggestions { get; set; }
}
