using MatchEngine.Api.Processor;
using Resume.Shared.Events;
using Resume.Shared.Messaging;
using System;
using System.Collections.Generic;
using System.Text;

namespace MatchEngine.Api.Consumer
{
    public class JobStatusUpdateConsumer: RabbitMqConsumerBase<JobUpdateStatusEvent>
    {
        protected override string QueueName => Queues.JobStatusUpdated;

        public JobStatusUpdateConsumer() : base()
        {
        }

        protected override async Task HandleMessage(
            JobUpdateStatusEvent message,
            IServiceProvider services)
        {
            try
            {
                var processor = services.GetRequiredService<StatusUpdateProcessor>();

                await processor.UpdateJobStatus(message.Id, message.Status, message.SessionId);
            }
            catch (Exception ex) {
                throw ex;
            }
        }
    }
}
