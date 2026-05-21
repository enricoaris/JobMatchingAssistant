using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Vector = Pgvector.Vector;

namespace Resume.Shared.Entities;

[Table("Resumes")]
public class Resumes
{
    [Key]
    public Guid Id { get; set; }
    public string FilePath { get; set; }
    public string Status { get; set; }
    public string? ContextText { get; set; }
    public Vector? Embedding { get; set; }
    public DateTime? CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public string? Filename { get; set; }

}
