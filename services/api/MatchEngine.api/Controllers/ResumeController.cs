using MatchEngine.Api.Helper;
using MatchEngine.Api.Hubs;
using MatchEngine.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;
using System.Runtime.InteropServices;

namespace MatchEngine.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class ResumeController : ControllerBase
{
    private readonly ResumeHelper _resumeHelper;
    public ResumeController(ResumeHelper resumeHelper)
    {
        _resumeHelper = resumeHelper;
    }

    [HttpPost("upload")]
    public async Task<IActionResult> Upload(UploadResumeRequest request)
    {
        try
        {
            var result = await _resumeHelper.UploadAsync(request);

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

    [HttpPost("embedding")]
    public async Task<IActionResult> UpdateEmbeddings(EmbeddingRequest request)
    {
        try
        {
            var result = await _resumeHelper.SaveEmbedding(request);

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
    public async Task<IActionResult> GetResumeList()
    {
        try
        {
            var result = await _resumeHelper.GetResumeList();

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
    [HttpDelete("delete")]
    public async Task<IActionResult> Delete([FromQuery] Guid id)
    {
        try
        {
            var result = await _resumeHelper.Delete(id);

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
