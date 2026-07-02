using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events
{
    public class ResumeUpdateStatusEvent
    {
        public Guid Id { get; set; }
        public int Status { get; set; }
        public string? SessionId { get; set; }
    }
}
