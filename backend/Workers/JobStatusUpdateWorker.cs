using MatchEngine.Api.Consumer;

namespace MatchEngine.Api.Workers;
public class JobStatusUpdateWorker : BackgroundService
{
    private readonly IServiceProvider _services;
    private readonly JobStatusUpdateConsumer _consumer;

    public JobStatusUpdateWorker(IServiceProvider services, JobStatusUpdateConsumer consumer)
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
