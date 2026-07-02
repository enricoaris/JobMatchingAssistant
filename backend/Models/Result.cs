namespace MatchEngine.Api.Models;
public class Result<T>
{
    public bool IsSuccess { get; set; }
    public string Message { get; set; }
    public T Data { get; set; }
    public List<string> Errors { get; set; } = new List<string>();

    public static Result<T> Success(T data, string message = "Success")
        => new() { IsSuccess= true, Message=message, Data=data};

    public static Result<T> Failure(string error)
        => new() { IsSuccess = false, Message = error, Errors = { error } };
}
