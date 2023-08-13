"""Callbacks involve notifying the client when a long-running 
task is completed. While FastAPI doesn't directly handle callbacks, 
you can design your API to accept a callback URL from the client 
and then trigger the callback when the task is done.
"""

from fastapi import FastAPI, BackgroundTasks
import time
import httpx

app = FastAPI()

# In-memory database to store operation status and callback URLs
operation_status = {}
callback_urls = {}


def perform_long_running_task(task_id):
    time.sleep(10)  # Simulating a long-running task
    operation_status[task_id] = "completed"
    if task_id in callback_urls:
        with httpx.Client() as client:
            client.post(callback_urls[task_id], json={"task_id": task_id})


@app.post("/start_task/")
async def start_task(background_tasks: BackgroundTasks, callback_url: str):
    task_id = len(operation_status) + 1
    operation_status[task_id] = "processing"
    callback_urls[task_id] = callback_url
    background_tasks.add_task(perform_long_running_task, task_id)
    return {"message": "Task started", "task_id": task_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
