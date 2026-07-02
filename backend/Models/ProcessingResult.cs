namespace MatchEngine.Api.Models;
public class ProcessingResult
{
    List<BatchedJob> Jobs { get; set; }
    public int Total { get; set; }
    public int Success { get; set; }
    public int Failed { get; set; }

    public class BatchedJob
    {
        public string Id { get; set; }
        public string Title { get; set; }
    }
}
