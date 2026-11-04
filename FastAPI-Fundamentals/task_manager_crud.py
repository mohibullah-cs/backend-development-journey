from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD application using FastAPI",
    version="1.0"
)


class Task(BaseModel):
    title: str = Field(min_length=3)
    description: str
    completed: bool = False


tasks = {}
next_id = 1


# CREATE
@app.post("/tasks")
def create_task(task: Task):
    global next_id

    tasks[next_id] = task.model_dump()

    response = {
        "id": next_id,
        **tasks[next_id]
    }

    next_id += 1

    return {
        "message": "Task created successfully",
        "task": response
    }


# READ ALL
@app.get("/tasks")
def get_tasks():
    return tasks


# READ ONE
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]


# UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task.model_dump()

    return {
        "message": "Task updated successfully",
        "task": tasks[task_id]
    }


# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }
