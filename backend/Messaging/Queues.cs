using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Messaging;

public static class Queues
{
    public const string ResumeUploaded = "resume-uploaded";
    public const string ResumeTextExtracted = "resume-text-extracted";
    public const string JobUploaded = "job-description-uploaded";
    public const string JobStatusUpdated = "job-status-updated";
    public const string ResumeStatusUpdated = "resume-status-updated";
    public const string ResumeEmbedded = "resume-embedded";
    public const string MatchingCompleted = "matching-completed";
}
