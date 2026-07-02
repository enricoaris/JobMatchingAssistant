using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events
{
    public class MatchingCompletedEvent
    {
        public Guid MatchId { get; set; }
        public Guid ResumeId { get; set; }
        public Guid JobId { get; set; }
        public Guid? SessionId { get; set; }
    }
}
