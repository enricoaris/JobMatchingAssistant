using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events
{
    public class ResumeEmbeddedEvent
    {
        public Guid ResumeId { get; set; }
        public Guid? SessionId { get; set; }
    }
}
