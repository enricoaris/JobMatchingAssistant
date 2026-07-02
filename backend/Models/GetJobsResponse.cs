namespace MatchEngine.Api.Models
{
    public class GetJobsResponse
    {
        public List<JobResponse> Jobs { get; set; }
    }

    public class JobResponse
    {
        public Guid Id {  get; set; }
        public string Name { get; set; }
        public int Status { get; set; }
        public bool Vector { get; set; }
    }
}
