using CsvHelper;
using CsvHelper.Configuration;
using MatchEngine.Api.Hubs;
using MatchEngine.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using Pgvector;
using RabbitMQ.Client;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;
using System.Net.NetworkInformation;
using static System.Net.Mime.MediaTypeNames;

namespace MatchEngine.Api.Helper;
public class JobHelper
{
    private readonly RabbitMqPublisher _publisher;
    private readonly AppDbContext _context;

    public JobHelper(RabbitMqPublisher publisher, AppDbContext context)
    {
        _publisher = publisher;
        _context = context;
    }
    public async Task<Result<ProcessingResult>> BatchUploadAsync(JobBatchUploadRequest request)
    {
        if (request.File == null || request.File.Length < 1)
        {
            return Result<ProcessingResult>.Failure("File is empty.");
        }

        using var stream = request.File.OpenReadStream();
        using var reader = new StreamReader(stream);

        var config = new CsvConfiguration(System.Globalization.CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true,
            TrimOptions = TrimOptions.Trim
        };

        using var csv = new CsvReader(reader, config);
        var result = new ProcessingResult { Total = 0, Success = 0, Failed = 0 };

        try
        {
            var jobRecords = csv.GetRecordsAsync<JobUploadData>();
            var processedJobs = new List<ProcessingResult.BatchedJob>();

            await foreach (var record in jobRecords)
            {
                result.Total++;

                JobUploadRequest jobUpload = new JobUploadRequest
                {
                    Description = record.Description,
                    Title = record.Title,
                    SessionId = request.SessionId
                };

                var processResult = await ProcessJobAsync(jobUpload);

                if (processResult.IsSuccess)
                {
                    result.Success++;
                    processedJobs.Add(new ProcessingResult.BatchedJob
                    {
                        Id = processResult.Data.ToString(),
                        Title = jobUpload.Title ?? String.Empty
                    });
                }
                else
                {
                    result.Failed++;
                    //TODO: Log Job Process Error
                }
            }

            return Result<ProcessingResult>.Success(result, "Processing Completed.");
        }
        catch (Exception ex)
        {
            throw ex;
        }
    }

    public async Task<Result<Guid>> ProcessJobAsync(JobUploadRequest jobUpload)
    {
        try
        {
            if (jobUpload == null || String.IsNullOrEmpty(jobUpload.Description) || string.IsNullOrEmpty(jobUpload.Title))
            {
                return Result<Guid>.Failure("Job cannot be empty.");
            }

            Guid Id = Guid.NewGuid();

            _context.Add(new Jobs
            {
                Id = Id,
                Title = jobUpload.Title,
                ContextText = jobUpload.Description,
                CreatedAt = DateTime.UtcNow
            });

            await _context.SaveChangesAsync();

            await _publisher.PublishAsync(Queues.JobUploaded, new JobUploadedMessage
            {
                Id = Id,
                Text = jobUpload.Description ?? "",
                SessionId = jobUpload.SessionId ?? "",
            });

            return Result<Guid>.Success(Id, "Upload Successful");
        }
        catch (Exception ex) {
            return Result<Guid>.Failure("An error occured when saving the job.");
        }
    }

    public async Task<Result<Guid>> SaveEmbedding(EmbeddingRequest request)
    {
        try
        {
            var job = _context
                .Jobs
                .FirstOrDefault(j => j.Id.Equals(request.Id));

            if (job == null)
            {
                return Result<Guid>.Failure("Job is not found.");
            }

            job.Embedding = new Vector(request.Embedding);
            job.UpdatedAt = DateTime.UtcNow;

            JobFeatures jobfeatures = new JobFeatures
            {
                EmbeddingNorm = request.EmbeddingNorm,
                SkillsMeta = request.SkillsMeta,
                EmbeddingStd = request.EmbeddingStd,
                ExperienceYears = request.ExperienceYears ?? -1,
                JobId = job.Id,
                Seniority = request.Seniority,
                Skills = request.Skills,
                Highlights = request.Highlights,
                Requirements = request.Requirements,
            };

            await _context.JobFeatures.AddAsync(jobfeatures);
            await _context.SaveChangesAsync();

            return Result<Guid>.Success(job.Id, "Saved successfully");
        }
        catch (Exception ex) {
            throw new Exception($"Internal error : {ex.Message}");
        }
    }
    public async Task<Result<GetJobsResponse>> GetJobs()
    {
        try
        {
            var jobs = _context.Jobs
                .OrderBy(j => j.CreatedAt)
                .Select(j => new JobResponse
                {
                    Id = j.Id,
                    Name = j.Title ?? "",
                    Status = j.Status ?? 0,
                    Vector = (bool)(j.Embedding != null)
                }).ToList();

            GetJobsResponse jobResponse = new GetJobsResponse
            {
                Jobs = jobs
            };

            return Result<GetJobsResponse>.Success(jobResponse, "Fetched successfully");
        }
        catch (Exception ex)
        {
            throw new Exception($"Internal error : {ex.Message}");
        }
    }
    public async Task<Result<Guid>> DeleteJob(Guid id)
    {
        try
        {
            var job = _context.Jobs.FirstOrDefault(j => j.Id.Equals(id));

            if (job == null)
            {
                throw new Exception("Job is not found.");
            }

            var jobFeatures = _context.JobFeatures.Where(jf => jf.JobId.Equals(job.Id)).ToList();

            _context.JobFeatures.RemoveRange(jobFeatures);
            _context.Jobs.Remove(job);

            await _context.SaveChangesAsync();

            return Result<Guid>.Success(job.Id, "Removed Successfully");
        }
        catch (Exception ex)
        {
            throw new Exception($"Internal error : {ex.Message}");
        }
    }
}
