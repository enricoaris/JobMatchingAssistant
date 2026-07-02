using MatchEngine.Api.Models;
using Npgsql;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Messaging;
using System.Text.RegularExpressions;

namespace MatchEngine.Api.Helper;

public class MatchHelper
{
    private readonly RabbitMqPublisher _publisher;
    private readonly AppDbContext _context;

    public MatchHelper(RabbitMqPublisher publisher, AppDbContext context)
    {
        _publisher = publisher;
        _context = context;
    }

    public async Task<Result<Guid>> UpdateInsights(UpdateInsightsRequest request)
    {
        Matches? match = _context.Matches.FirstOrDefault(m => m.MatchId.ToString().Equals(request.MatchId));

        if (match == null) Result<Guid>.Failure("Match is not found.");

        match.Suggestions = request.Suggestions;
        match.MatchLevel = request.MatchLevel;
        match.KeyGaps = request.KeyGaps;
        match.Assessment = request.Assessment;
        
        await _context.SaveChangesAsync();

        return Result<Guid>.Success(match.MatchId);
    }

    public async Task<Result<GetMatchesResponse>> GetMatches(Guid resumeId)
    {
        var matches = _context.Matches.Where(m => m.ResumeId.Equals(resumeId));

        if (!matches.Any()) return Result<GetMatchesResponse>.Failure("No match is found.");

        var jobIds = matches.Select(m => m.JobId).Distinct().ToList();
        var jobsLookup = _context.Jobs
            .Where(j => jobIds.Contains(j.Id))
            .ToDictionary(j => j.Id, j => j.Title);

        List<MatchDetail> matchList = matches.Select(match => new MatchDetail(
            match.JobId.ToString(),
            jobsLookup.GetValueOrDefault(match.JobId) ?? "",
            match.Score,
            match.MatchLevel ?? "",
            match.Assessment ?? "",
            match.KeyGaps ?? new List<string>(),
            match.Suggestions ?? new List<string>()
        )).ToList();

        return Result<GetMatchesResponse>.Success(new GetMatchesResponse(matchList));
    }

    public async Task<Result<Guid>> DeleteMatches(Guid resumeId)
    {
        var matches = _context.Matches.Where(m => m.ResumeId.Equals(resumeId));

        if (matches.Any()) return Result<Guid>.Failure("No matches are found.");

        _context.Matches.RemoveRange(matches);

        await _context.SaveChangesAsync();

        return Result<Guid>.Success(resumeId);
    }
}
