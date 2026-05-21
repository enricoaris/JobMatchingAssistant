
import asyncio
from messaging.rabbit_client import RabbitClient
from enums import QueueName
from processing_service import process_job, process_resume, process_insights

async def main():
    client = RabbitClient()
    await client.connect()

    try:
        await asyncio.gather(
            client.consume(QueueName.RESUME_EXTRACTED, process_resume),
            client.consume(QueueName.JOB_UPLOADED, process_job),
            client.consume(QueueName.MATCHING_COMPLETED, process_insights)
        )
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())