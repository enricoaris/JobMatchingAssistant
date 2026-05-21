using RabbitMQ.Client;
using System.Text;
using System.Text.Json;

namespace Resume.Shared.Messaging;
public class RabbitMqPublisher: IDisposable
{
    private readonly ConnectionFactory _factory;
    private IConnection _connection;
    private IChannel _channel;

    public RabbitMqPublisher()
    {
        var rabbitHost = Environment.GetEnvironmentVariable("RABBITMQ_HOST") ?? "localhost";

        _factory = new ConnectionFactory()
        {
            HostName = rabbitHost
        };
    }

    private async Task EnsureConnection()
    {
        if (_connection == null)
            _connection = await _factory.CreateConnectionAsync();
        if (_channel == null)
            _channel = await _connection.CreateChannelAsync();
    }

    public async Task PublishAsync<T>(string queue, T message)
    {
        await EnsureConnection();

        await _channel!.QueueDeclareAsync(
            queue: queue,
            durable: false,
            exclusive: false,
            autoDelete: false,
            arguments: null
        );

        var json = JsonSerializer.Serialize(message);
        var body = Encoding.UTF8.GetBytes(json);

        await _channel.BasicPublishAsync(
            exchange: "",
            routingKey: queue,
            mandatory: false,
            body: body
        );
    }

    public async Task PublishFanoutAsync<T>(string exchangeName, T message)
    {
        await EnsureConnection();

        await _channel.ExchangeDeclareAsync(
            exchange: exchangeName,
            type: ExchangeType.Fanout,
            durable: true,
            autoDelete: false,
            arguments: null
        );

        var json = JsonSerializer.Serialize(message);
        var body = Encoding.UTF8.GetBytes(json);

        var props = new BasicProperties
        {
            Persistent = true
        };

        await _channel.BasicPublishAsync(
            exchange: exchangeName,
            routingKey: "",
            mandatory: false,
            basicProperties: props,
            body: body
        );
    }

    public void Dispose()
    {
        _channel?.Dispose();
        _connection?.Dispose();
    }
}
