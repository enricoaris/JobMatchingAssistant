using MatchEngine.Api.Models;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text;

namespace Resume.Shared.Entities;

[Table("ResumeFeatures")]
public class ResumeFeatures
{
    [Key]
    public Guid Id { get; set; }
    public Guid ResumeId { get; set; }
    [Column(TypeName = "jsonb")]
    public List<string>? Skills { get; set; }
    [Column(TypeName = "jsonb")]
    public Dictionary<string, SkillMeta>? SkillsMeta { get; set; }
    public int ExperienceYears { get; set; }
    public string? Seniority { get; set; }
    public float? EmbeddingNorm { get; set; }
    public float? EmbeddingStd { get; set; }
    public List<string>? Requirements { get; set; }
    public List<string>? Highlights { get; set; }
}
