using System;
using System.Collections.Generic;
using System.Text;

namespace MatchEngine.Api.Models
{
    public class SkillMeta
    {
        public SkillMeta() { }
        public List<string> Source { get; set; } = new();
        public double Confidence { get; set; }
    }
}
