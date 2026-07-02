using MatchEngine.Api.Processor;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Consumer
{
    public class ResumeEmbeddedConsumer : RabbitMqConsumerBase<ResumeEmbeddedEvent>
    {
        protected override string QueueName => Queues.ResumeEmbedded;

        public ResumeEmbeddedConsumer() : base()
        {
        }

        protected override async Task HandleMessage(
            ResumeEmbeddedEvent message,
            IServiceProvider services)
        {
            try
            {
                var processor = services.GetRequiredService<MatchingProcessor>();

                await processor.processMatching(message);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }
}
