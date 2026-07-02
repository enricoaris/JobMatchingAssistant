using MatchEngine.Api.Hubs;
using Microsoft.AspNetCore.SignalR;
using Resume.Shared.Data;
using Resume.Shared.Events;
using Resume.Shared.Messaging;
using System;
using System.Collections.Generic;
using System.Text;

namespace MatchEngine.Api.Processor
{
    public class StatusUpdateProcessor
    {
        private readonly AppDbContext _dbContext;
        private readonly IHubContext<ProcessingHub> _hubContext;
        public StatusUpdateProcessor(AppDbContext dbContext, IHubContext<ProcessingHub> hubContext)
        {
            _dbContext = dbContext;
            _hubContext = hubContext;
        }

        public async Task UpdateJobStatus(Guid jobId, int status, string sessionId)
        {
            try
            {
                var job = _dbContext.Jobs.FirstOrDefault(j => j.Id.Equals(jobId));

                if (job == null) return;

                job.Status = status;

                await _dbContext.SaveChangesAsync();

                await _hubContext.Clients.Group(sessionId).SendAsync("jobStatusUpdate", new JobStatusUpdateEvent
                {
                    Id = jobId,
                    Status = status,
                });
            }
            catch (Exception ex) {
                throw ex;
            }
        }

        public async Task UpdateResumeStatus(Guid resumeId, int status, string sessionId)
        {
            try
            {
                var resume = _dbContext.Resumes.FirstOrDefault(r => r.Id.Equals(resumeId));

                if (resume == null) return;

                resume.Status = status;

                await _dbContext.SaveChangesAsync();

                await _hubContext.Clients.Group(sessionId).SendAsync("resumeStatusUpdate", new ResumeUpdateStatusEvent
                {
                    Id = resumeId,
                    Status = status,
                    SessionId = sessionId
                });
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }
}
