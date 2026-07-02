using Pgvector;

namespace Resume.Shared.Events;
public class MatchRequestMessage
{
    public Vector? JobEmbedding { get; set; }
    public Vector? ResumeEmbedding { get; set; }
}
