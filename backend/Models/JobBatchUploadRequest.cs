namespace MatchEngine.Api.Models;

public class JobBatchUploadRequest
{
    public IFormFile File { get; set; }
    public string? SessionId { get; set; } = String.Empty;
}
