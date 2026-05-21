namespace MatchEngine.Api.Models;
public class UploadResumeRequest
{
    public IFormFile File {  get; set; }
    public string? SessionId { get; set; }
}
