import aio_pika
from settings import *
import inspect
from enums.queue_name import QueueName 
import json

class RabbitClient:
    def __init__(self):
        self.connection = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            f"amqp://guest:guest@{RABBITMQ_HOST}/"
        )
        print("Successfully connected to RabbitMQ.")
        return self

    async def consume(self, queue_name: QueueName, callback_func):
        if not self.connection:
            await self.connect()

        async with self.connection.channel() as channel:
            await channel.set_qos(prefetch_count=1)

            queue = await channel.declare_queue(queue_name, durable=False)
            print(f" [*] Waiting for messages in {queue_name}.")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    # Use context manager to handle automatic ACKs
                    async with message.process(requeue=True):
                        try:
                            res = callback_func(message, self)

                            if inspect.iscoroutine(res):
                                response = await res
                            else:
                                response = res

                            if response.status_code != 200:
                                try:
                                    error_details = response.json()
                                except Exception:
                                    error_details = response.text
                                error_msg = f"Handler failed with status {response.status_code}. Details: {error_details}"

                                print(error_msg)
                                print(error_details)
                                raise Exception(error_msg)

                        except Exception as e:
                            print(f"Error processing message from {queue_name}: {e}")
                            raise

    async def publish(self, queue_name: QueueName, body: dict):
        channel = await self.connection.channel()

        routing_key = queue_name.value

        await channel.declare_queue(routing_key, durable=False)

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(body).encode()),
            routing_key=routing_key
        )

        await channel.close()

    async def close(self):
        if self.connection:
            await self.connection.close()
    