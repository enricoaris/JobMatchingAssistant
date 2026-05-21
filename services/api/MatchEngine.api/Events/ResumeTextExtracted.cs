using System;
using System.Collections.Generic;
using System.Text;

namespace Resume.Shared.Events;

public class ResumeTextExtracted
{
    public Guid Id { get; set; }
    public string Text { get; set; } = string.Empty;
    public string SessionId { get; set; } = string.Empty;

}
