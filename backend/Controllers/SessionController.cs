using Microsoft.AspNetCore.Mvc;

namespace MatchEngine.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class SessionController:ControllerBase
{
    [HttpPost]
    public IActionResult createSession()
    {
        var sessionId = Guid.NewGuid().ToString();

        return Ok(new
        {
            sessionId
        });
    }
}
