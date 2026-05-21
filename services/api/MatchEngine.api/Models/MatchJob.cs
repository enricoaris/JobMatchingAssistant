namespace MatchEngine.Api.Models;

public class MatchJob
{
    public Guid Id { get; set; }
    public string Status { get; set; }
    public string Stage { get; set; }
    public string? ResultJson { get; set; }
}
