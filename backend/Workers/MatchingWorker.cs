using MatchEngine.Api.Consumer;

namespace MatchEngine.Api.Workers
{
    public class MatchingWorker: BackgroundService
    {
        private readonly IServiceProvider _services;
        private readonly ResumeEmbeddedConsumer _consumer;

        public MatchingWorker(IServiceProvider services, ResumeEmbeddedConsumer consumer)
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
