using MatchEngine.Api.Consumer;

namespace MatchEngine.Api.Workers
{
    public class ResumeStatusUpdateWorker: BackgroundService
    {
        private readonly IServiceProvider _services;
        private readonly ResumeStatusUpdateConsumer _consumer;

        public ResumeStatusUpdateWorker(IServiceProvider services, ResumeStatusUpdateConsumer consumer)
        {
            _services = services;
            _consumer = consumer;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            await _consumer.StartAsync(_services);

            await Task.Delay(Timeout.Infinite, stoppingToken);
        }
    }
}
