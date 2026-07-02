using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events;

public class ResumeUploadedEvent
{
    public Guid ResumeId { get; set; }
    public string SessionId { get; set; }
}
