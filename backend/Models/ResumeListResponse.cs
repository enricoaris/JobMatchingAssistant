namespace MatchEngine.Api.Models
{
    public class ResumeListResponse
    {
        public List<ResumeProfile> Resume { get; set; } = new List<ResumeProfile>();
        public class ResumeProfile
        {
            public string? Title { get; set; }
            public int? Status { get; set; }
            public Guid? ResumeId { get; set; }
        }
    }
}
