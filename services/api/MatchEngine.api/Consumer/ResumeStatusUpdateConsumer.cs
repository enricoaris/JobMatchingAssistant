using MatchEngine.Api.Processor;
using Resume.Shared.Events;
using Resume.Shared.Messaging;

namespace MatchEngine.Api.Consumer
{
    public class ResumeStatusUpdateConsumer : RabbitMqConsumerBase<ResumeUpdateStatusEvent>
    {
        protected override string QueueName => Queues.ResumeStatusUpdated;

        public ResumeStatusUpdateConsumer() : base()
        {
        }

        protected override async Task HandleMessage(
            ResumeUpdateStatusEvent message,
            IServiceProvider services)
        {
            try
            {
                var processor = services.GetRequiredService<StatusUpdateProcessor>();

                await processor.UpdateResumeStatus(message.Id, message.Status, message.SessionId);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }
}
