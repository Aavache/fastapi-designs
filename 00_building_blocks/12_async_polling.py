"""In polling we let the user know the status of the 
long-running task
"""
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

# In-memory database to store operation status
operation_status = {}


def perform_long_running_task(task_id):
    time.sleep(10)  # Simulating a long-running task
    operation_status[task_id] = "completed"


@app.post("/start_task/")
async def start_task(background_tasks: BackgroundTasks):
    task_id = len(operation_status) + 1
    operation_status[task_id] = "processing"
    background_tasks.add_task(perform_long_running_task, task_id)
    return {"message": "Task started", "task_id": task_id}


@app.get("/check_task/{task_id}")
async def check_task(task_id: int):
    status = operation_status.get(task_id, "not found")
    return {"task_id": task_id, "status": status}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
