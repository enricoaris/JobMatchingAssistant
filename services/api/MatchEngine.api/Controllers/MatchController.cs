using MatchEngine.Api.Helper;
using MatchEngine.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Pgvector.EntityFrameworkCore;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class MatchController : ControllerBase
{
    private readonly AppDbContext _context;
    private readonly MatchHelper _matchHelper;

    public MatchController(AppDbContext context, MatchHelper matchHelper)
    {
        _context = context;
        _matchHelper = matchHelper;
    }

    [HttpPost("insights")]
    public async Task<IActionResult> UpdateInsights(UpdateInsightsRequest request)
    {
        try
        {
            var result = await _matchHelper.UpdateInsights(request);

            if (result.IsSuccess)
            {
                return Ok(result.Data);
            }
            else
            {
                return BadRequest(result.Message);
            }
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
    [HttpGet]
    public async Task<IActionResult> GetMatches([FromQuery] Guid resumeId)
    {
        try
        {
            var result = await _matchHelper.GetMatches(resumeId);

            if (result.IsSuccess)
            {
                return Ok(result.Data);
            }
            else
            {
                return BadRequest(result.Message);
            }
        }
        catch(Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
    [HttpDelete]
    public async Task<IActionResult> DeleteMatches([FromQuery] Guid resumeId)
    {
        try
        {
            var result = await _matchHelper.DeleteMatches(resumeId);

            if (result.IsSuccess)
            {
                return Ok(result.Data);
            }
            else
            {
                return BadRequest(result.Message);
            }
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }
}
