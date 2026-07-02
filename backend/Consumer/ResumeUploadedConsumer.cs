using MatchEngine.Api.Processor;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Consumer;
public class ResumeUploadedConsumer : RabbitMqConsumerBase<ResumeUploadedEvent>
{
    protected override string QueueName => Queues.ResumeUploaded;

    public ResumeUploadedConsumer() : base()
    {
    }

    protected override async Task HandleMessage(
        ResumeUploadedEvent message,
        IServiceProvider services)
    {
        var processor = services.GetRequiredService<ResumeProcessor>();

        await processor.ProcessResume(message.ResumeId, message.SessionId);
    }
}

