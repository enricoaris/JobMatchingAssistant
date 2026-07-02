namespace MatchEngine.Api.Models
{
    public class JobStatsResult
    {
        public int Completed { get; set; }
        public int OnProgress { get; set; }
        public int Failed { get; set; }
        public int Total { get; set; }
    }
}
