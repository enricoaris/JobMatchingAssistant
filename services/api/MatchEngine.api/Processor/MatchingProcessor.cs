using MatchEngine.Api.Models;
using Npgsql;
using Resume.Shared.Data;
using Resume.Shared.Entities;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Processor
{
    public class MatchingProcessor
    {
        private readonly RabbitMqPublisher _publisher;
        private readonly AppDbContext _context;
        private readonly NpgsqlDataSource _dataSource;
        private readonly int TOPN = 30;
        private readonly double threshold = 0; // threshold is disabled

        public MatchingProcessor(RabbitMqPublisher publisher, AppDbContext context, NpgsqlDataSource dataSource)
        {
            _publisher = publisher;
            _context = context;
            _dataSource = dataSource;
        }

        public async Task<Result<List<MatchScore>>> processMatching(ResumeEmbeddedEvent request)
        {
            try
            {
                List<MatchScore> topMatchScoreMatches = new List<MatchScore>();
                List<MatchScore> topMatches = await GetTopMatches(request.ResumeId, TOPN);

                var filtered = topMatches.Where(e => e.Score >= threshold).ToList();

                if (filtered.Any())
                {
                    var filteredJobId = filtered.Select(e => e.JobId).ToList();

                    var resumeMeta = _context.ResumeFeatures.Where(e => e.ResumeId.Equals(request.ResumeId)).FirstOrDefault();
                    var jobsMeta = _context.JobFeatures.Where(e => filteredJobId.Contains(e.JobId)).ToList();

                    foreach (var jobMeta in jobsMeta)
                    {
                        var vectorScore = filtered.Where(r => r.JobId.Equals(jobMeta.JobId)).Select(r => r.Score).FirstOrDefault();
                        var skillScore = CalculateSkillScore(resumeMeta.Skills, jobMeta.Skills);
                        var experienceScore = CalculateExperienceScore(resumeMeta.ExperienceYears, jobMeta.ExperienceYears);
                        var ruleScore = skillScore * 0.5 + experienceScore * 0.2 + vectorScore * 0.3;

                        var missingSkills = GetMissingSkills(resumeMeta.Skills, jobMeta.Skills);

                        topMatchScoreMatches.Add(new MatchScore {
                            Score = ruleScore,
                            JobId = jobMeta.JobId,
                            MissingSkills = missingSkills
                        });
                    }

                    topMatchScoreMatches = topMatchScoreMatches
                        .OrderByDescending(e => e.Score)
                        .Take(10)
                        .ToList();

                    var matches = new List<Matches>();
                    var matchEvents = new List<MatchingCompletedEvent>();

                    foreach (MatchScore match in topMatchScoreMatches)
                    {
                        var newId = Guid.NewGuid();

                        matches.Add(new Matches
                        {
                            MatchId = newId,
                            JobId = match.JobId,
                            ResumeId = request.ResumeId,
                            CreatedAt = DateTime.UtcNow,
                            Score = (float?)match.Score,
                            MissingSkills = match.MissingSkills
                        });

                        matchEvents.Add(new MatchingCompletedEvent
                        {
                            MatchId = newId
                        });
                    }

                    await _context.Matches.AddRangeAsync(matches);

                    await _context.SaveChangesAsync();

                    foreach(var matchEvent in matchEvents)
                    {
                        await _publisher.PublishAsync(
                            Queues.MatchingCompleted,
                            matchEvent
                        );
                    }
                }

                return Result<List<MatchScore>>.Success(topMatchScoreMatches, "Success");
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        public async Task<List<MatchScore>> GetTopMatches(Guid resumeId, int topN)
        {
            Resumes? resume = _context.Resumes.FirstOrDefault(e => e.Id.Equals(resumeId));

            if (resume == null || resume.Embedding == null)
            {
                throw new Exception("Resume is not found.");
            }

            await using var cmd = _dataSource.CreateCommand(@"
                select j.""Id"" , 1 - (j.""Embedding""  <=> @query) as Score
                from ""Jobs"" j
                order by j.""Embedding"" <=> @query
                limit @topN
            ");

            cmd.Parameters.AddWithValue("query", resume.Embedding);
            cmd.Parameters.AddWithValue("topN", topN);

            var results = new List<MatchScore>();

            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                results.Add(new MatchScore
                {
                    JobId = reader.GetGuid(0),
                    Score = reader.GetDouble(1)
                });
            }

            return results;
        }

        public double CalculateSkillScore(List<string> resumeSkills, List<string> jobSkills)
        {
            int match = jobSkills.Count(e =>
                resumeSkills.Contains(e, StringComparer.OrdinalIgnoreCase)
            );

            return (double)match / jobSkills.Count;
        }

        public List<string> GetMissingSkills(List<string> resumeSkills, List<string> jobSkills)
        {
            if (resumeSkills == null) return jobSkills;
            if (jobSkills == null) return new List<string>();

            return jobSkills.Except(resumeSkills, StringComparer.OrdinalIgnoreCase).ToList();
        }

        public double CalculateExperienceScore(int? resumeExp, int? jobMinExp)
        {
            if (resumeExp == null || jobMinExp == null || resumeExp < 0 || jobMinExp < 0) return 0;
            if (resumeExp >= jobMinExp) return 1.0;

            return (double)((double)resumeExp / jobMinExp);
        }
    }
}