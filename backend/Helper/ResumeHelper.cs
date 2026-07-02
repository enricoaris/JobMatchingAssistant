using MatchEngine.Api.Hubs;
using MatchEngine.Api.Models;
using Microsoft.AspNetCore.SignalR;
using Microsoft.EntityFrameworkCore;
using Pgvector;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;
using static MatchEngine.Api.Models.ResumeListResponse;

namespace MatchEngine.Api.Helper;
public class ResumeHelper
{
    private readonly RabbitMqPublisher _publisher;
    private readonly AppDbContext _context;
    private readonly IHubContext<ProcessingHub> _hubContext;
    private readonly string _uploadPath = Path.Combine(Directory.GetCurrentDirectory(), "Uploads");

    public ResumeHelper(RabbitMqPublisher publisher, AppDbContext context, IHubContext<ProcessingHub> processingHub)
    {
        _publisher = publisher;
        _context = context;
        _hubContext = processingHub;
        if (!Directory.Exists(_uploadPath)) Directory.CreateDirectory(_uploadPath);
    }

    public async Task<Result<ResumeListResponse>> GetResumeList()
    {
        var result = new ResumeListResponse();
        result.Resume = _context.Resumes.OrderBy(r => r.CreatedAt).Select(r => new ResumeProfile
        {
            ResumeId = r.Id,
            Status = r.Status,
            Title = r.Filename
        }).ToList();

        return Result<ResumeListResponse>.Success(result);
    }
    public async Task<Result<Guid>> UploadAsync(UploadResumeRequest request)
    {
        try
        {
            if (request.File == null || request.File.Length == 0)
            {
                return Result<Guid>.Failure("No File Uploaded.");
            }

            var generatedFileName = $"{Guid.NewGuid()}{Path.GetExtension(request.File.FileName)}";
            var filePath = Path.Combine(_uploadPath, generatedFileName);

            var resume = new Resumes
            {
                FilePath = filePath,
                CreatedAt = DateTime.UtcNow,
                Status = 1, // Stands for Uploaded
                Filename = request.File.FileName
            };

            _context.Add(resume);
            await _context.SaveChangesAsync();

            await _publisher.PublishAsync(Queues.ResumeUploaded, new ResumeUploadedEvent
            {
                ResumeId = resume.Id,
                SessionId = request.SessionId ?? ""
            });

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await request.File.CopyToAsync(stream);
            };

            return Result<Guid>.Success(resume.Id, "Upload Successful.");
        }
        catch (Exception ex)
        {
            throw new Exception($"Internal error : {ex.Message}");
        }
    }

    public async Task<Result<Guid>> SaveEmbedding(EmbeddingRequest request)
    {
        try
        {
            var resume = _context
                .Resumes
                .FirstOrDefault(j => j.Id.Equals(request.Id));

            if (resume == null)
            {
                return Result<Guid>.Failure("Job is not found.");
            }

            resume.Embedding = new Vector(request.Embedding);
            resume.UpdatedAt = DateTime.UtcNow;

            ResumeFeatures resumefeatures = new ResumeFeatures
            {
                EmbeddingNorm = request.EmbeddingNorm,
                SkillsMeta = request.SkillsMeta,
                EmbeddingStd = request.EmbeddingStd,
                ExperienceYears = request.ExperienceYears ?? -1,
                ResumeId = resume.Id,
                Seniority = request.Seniority,
                Skills = request.Skills,
                Requirements = request.Requirements,
                Highlights = request.Highlights,
            };

            await _context.ResumeFeatures.AddAsync(resumefeatures);
            await _context.SaveChangesAsync();

            await _publisher.PublishAsync(Queues.ResumeEmbedded, new ResumeEmbeddedEvent
            {
                ResumeId = resume.Id,
                SessionId = request.SessionId ?? null
            });

            return Result<Guid>.Success(resume.Id, "Saved successfully");
        }
        catch (Exception ex)
        {
            throw new Exception($"Internal error : {ex.Message}");
        }
    }

    public async Task<Result<Guid>> Delete(Guid id)
    {
        var resume = _context.Resumes.FirstOrDefault(r => r.Id.Equals(id));

        if (resume == null) return Result<Guid>.Failure("Resume is not found.");

        var features = _context.ResumeFeatures.Where(r => r.ResumeId.Equals(id)).FirstOrDefault();

        if( features != null ) _context.Remove(features);

        _context.Remove(resume);
        await _context.SaveChangesAsync();

        return Result<Guid>.Success(id);
    }
}
