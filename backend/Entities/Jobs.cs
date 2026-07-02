using Pgvector;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text;

namespace Resume.Shared.Entities;

[Table("Jobs")]
public class Jobs
{
    [Key]
    public Guid Id { get; set; }
    public string? Title { get; set; }
    public string? ContextText { get; set; }
    public int? Status { get; set; }
    public Vector? Embedding { get; set; }
    public DateTime? CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
