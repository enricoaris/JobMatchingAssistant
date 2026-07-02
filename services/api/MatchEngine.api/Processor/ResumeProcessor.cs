using MatchEngine.Api.Helper;
using Microsoft.EntityFrameworkCore;
using Resume.Shared.Data;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Processor
{
    public class ResumeProcessor
    {
        private readonly AppDbContext _dbContext;
        private readonly PdfHelper _pdfHelper;
        private readonly RabbitMqPublisher _publisher;

        public ResumeProcessor(AppDbContext dbContext
            , PdfHelper pdfHelper
            , RabbitMqPublisher publisher
            )
        {
            _dbContext = dbContext;
            _publisher = publisher;
            _pdfHelper = pdfHelper;
        }

        public async Task ProcessResume(Guid resumeId, string sessionId)
        {
            var resume = await _dbContext.Resumes
                    .Where(r => r.Id.Equals(resumeId))
                    .FirstOrDefaultAsync();

            if (resume != null)
            {
                var path = resume.FilePath;

                if (File.Exists(path))
                {
                    var extractedText = _pdfHelper.Extract(path);

                    resume.ContextText = extractedText;
                    resume.Status = 10; // Stands For Text Extracted
                    resume.UpdatedAt = DateTime.UtcNow;

                    await _dbContext.SaveChangesAsync();

                    await _publisher.PublishAsync(Queues.ResumeTextExtracted, new ResumeTextExtracted
                    {
                        Id = resumeId,
                        Text = extractedText,
                        SessionId = sessionId
                    });
                }
                else
                {
                    //logger.LogWarning($"File not found {path}");
                }
            }
        }
    }

}
