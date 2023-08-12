from fastapi import FastAPI
import asyncio

app = FastAPI()

async def long_running_task():
    await asyncio.sleep(5)  # Simulate a long-running operation
    return "Task completed"

@app.get("/async-task")
async def async_task():
    result = await long_running_task()
    return {"message": result}

# Callback
@app.get("/start-long-task-with-callback")
async def start_long_task_with_callback(callback_url: str):
    task_id = "unique_task_id"  # Generate a unique task ID
    asyncio.create_task(long_running_task_with_id_and_callback(task_id, callback_url))
    return {"task_id": task_id}
