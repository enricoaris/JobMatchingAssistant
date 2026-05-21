using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events
{
    public class JobStatusUpdateEvent
    {
        public Guid Id {  get; set; }
        public string Status { get; set; } = string.Empty;
    }
}
