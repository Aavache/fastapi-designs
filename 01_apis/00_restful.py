from fastapi import FastAPI, HTTPException, Path, Body
from typing import List


app = FastAPI()
tasks = []


class Task:
    """Task model"""
    def __init__(self, id: int, title: str, description: str, done: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., description="ID of the task to retrieve")):
    if task_id < 1 or task_id > len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id - 1]


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int = Path(..., description="ID of the task to update"), task: Task = Body(...)):
    if task_id < 1 or task_id > len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id - 1] = task
    return task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int = Path(..., description="ID of the task to delete")):
    if task_id < 1 or task_id > len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    removed_task = tasks.pop(task_id - 1)
    return removed_task


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)