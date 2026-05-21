namespace MatchEngine.Api.Models
{
    public class EmbeddingRequest
    {
        public Guid Id { get; set; }
        public float[] Embedding { get; set; }
        public float? EmbeddingStd { get; set; }
        public float? EmbeddingNorm { get; set; }
        public List<string>? Skills { get; set; }
        public Dictionary<string, SkillMeta>? SkillsMeta { get; set; }
        public int? ExperienceYears { get; set; }
        public string? Seniority { get; set; }
        public List<string>? Requirements { get; set; }
        public List<string>? Highlights { get; set; }
        public string? SessionId { get; set; }
    }
}
