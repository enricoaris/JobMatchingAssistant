using MatchEngine.Api.Consumer;

namespace MatchEngine.Api.Workers;

public class ResumeTextWorker: BackgroundService
{
    private readonly IServiceProvider _services;
    private readonly ResumeUploadedConsumer _consumer;

    public ResumeTextWorker(IServiceProvider services, ResumeUploadedConsumer consumer)
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
