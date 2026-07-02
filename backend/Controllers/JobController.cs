using CsvHelper;
using CsvHelper.Configuration;
using MatchEngine.Api.Helper;
using MatchEngine.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Pgvector;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Controllers;


[ApiController]
[Route("[controller]")]
public class JobController: ControllerBase
{
    private readonly JobHelper _jobHelper;

    public JobController(JobHelper jobHelper)
    {
        _jobHelper = jobHelper;
    }

    [HttpPost("batch-upload")]
    public async Task<IActionResult> BatchUpload(JobBatchUploadRequest request)
    {
        try
        {
            var result = await _jobHelper.BatchUploadAsync(request);

            if (result.IsSuccess)
            {
                return Ok(result.Data);
            }
            else
            {
                return BadRequest(result.Message);
            }
        }
        catch (Exception ex) {
            return StatusCode(500, $"Internal server error: {ex.Message}");
        }
    }

    [HttpPost("upload")]
    public async Task<IActionResult> Upload([FromBody] JobUploadRequest jobUpload)
    {
        try
        {
            var result = await _jobHelper.ProcessJobAsync(jobUpload);

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
    public async Task<IActionResult> UpdateEmbedding(EmbeddingRequest request)
    {
        try
        {
            var result = await _jobHelper.SaveEmbedding(request);

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
    public async Task<IActionResult> GetJobs()
    {
        try
        {
            var result = await _jobHelper.GetJobs();

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
    [HttpDelete]
    public async Task<IActionResult> DeleteJob(Guid id)
    {
        try
        {
            var result = await _jobHelper.DeleteJob(id);

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
