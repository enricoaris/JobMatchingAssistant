using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text;

namespace Resume.Shared.Entities;

[Table("Matches")]
public class Matches
{
    [Key]
    public Guid MatchId { get; set; }
    public Guid ResumeId { get; set; }
    public Guid JobId { get; set; }
    public float Score { get; set; }
    public List<string>? Suggestions { get; set; }
    public List<string>? MissingSkills { get; set; }
    [Column("match_level")]
    public string? MatchLevel { get; set; }

    [Column("assessment")]
    public string? Assessment { get; set; }

    [Column("key_gaps")]
    public List<string>? KeyGaps { get; set; }
    public DateTime? CreatedAt { get; set; }
}
