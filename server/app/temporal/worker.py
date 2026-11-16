import asyncio
from concurrent.futures import ThreadPoolExecutor
from temporalio.client import Client
from temporalio.worker import Worker
from app.temporal.workflows import ApprovalWorkflow
from app.temporal.activities import update_request_status

async def main():
    client = await Client.connect("localhost:7233")
    
    # We create a thread pool for our synchronous database activity
    with ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker = Worker(
            client,
            task_queue="approval-task-queue",
            workflows=[ApprovalWorkflow],
            activities=[update_request_status],
            activity_executor=activity_executor, # <- Pass the executor here
        )
        
        print("Starting Temporal Worker. Listening for tasks on 'approval-task-queue'...")
        await worker.run()

if __name__ == "__main__":
    asyncio.run(main())