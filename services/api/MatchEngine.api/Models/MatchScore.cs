namespace MatchEngine.Api.Models;
public class MatchScore
{
    public Guid JobId { get; set; }
    public double Score { get; set; }
    public List<string> MissingSkills { get; set; }
}
