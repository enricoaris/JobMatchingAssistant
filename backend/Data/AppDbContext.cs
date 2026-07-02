using MatchEngine.Api.Models;
using Microsoft.EntityFrameworkCore;
using Resume.Shared.Entities;
using System.Text.Json;

namespace Resume.Shared.Data;
public class AppDbContext: DbContext
{
    public DbSet<Resumes> Resumes => Set<Resumes>();
    public DbSet<Jobs> Jobs => Set<Jobs>();
    public DbSet<Matches> Matches => Set<Matches>();
    public DbSet<ResumeFeatures> ResumeFeatures => Set<ResumeFeatures>();
    public DbSet<JobFeatures> JobFeatures => Set<JobFeatures>(); 

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.HasPostgresExtension("vector");

        modelBuilder.Entity<Resumes>(entity =>
        {
            entity.HasKey(x => x.Id);
            entity.Property(x => x.Embedding)
                .HasColumnType("vector(1536)");
        });

        modelBuilder.Entity<JobFeatures>()
            .Property(e => e.SkillsMeta)
            .HasConversion(
                v => JsonSerializer.Serialize(v, (JsonSerializerOptions)null),
                v => JsonSerializer.Deserialize<Dictionary<string, SkillMeta>>(v, (JsonSerializerOptions)null)
            )
            .HasColumnType("jsonb");

        modelBuilder.Entity<JobFeatures>()
            .Property(e => e.Skills)
            .HasColumnType("jsonb");

        modelBuilder.Entity<ResumeFeatures>()
            .Property(e => e.Skills)
            .HasColumnType("jsonb");

        modelBuilder.Entity<ResumeFeatures>()
            .Property(e => e.SkillsMeta)
            .HasColumnType("jsonb");
    }
}
