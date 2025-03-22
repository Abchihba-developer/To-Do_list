import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List

from config import settings
import shemas
import crud


app = FastAPI()


@app.post(path="/tasks/", response_model=shemas.Task)
async def create_task(task: shemas.TaskCreate) -> shemas.Task:
    res = await crud.create_task(title=task.title, description=task.description, completed=task.completed)
    return res


@app.get(path="/tasks/", response_model=List[shemas.Task])
async def read_tasks(skip: int = 0, limit: int = 10) -> List[shemas.Task]:
    tasks = await crud.get_tasks(skip=skip, limit=limit)
    return tasks


@app.get(path="/task/{task_id}", response_model=shemas.Task)
async def read_task_by_id(task_id: int) -> shemas.Task:
    task = await crud.get_task(task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put(path="/task/{task_id}", response_model=shemas.Task)
async def update_task_by_id(task_id: int, task_update: shemas.TaskUpdate) -> shemas.Task:
    task = await crud.update_task(task_id=task_id,
                                  title=task_update.title,
                                  description=task_update.description,
                                  completed=task_update.completed)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete(path="/task/{task_id}", response_model=shemas.Task)
async def delete_task_by_id(task_id: int) -> shemas.Task:
    deleted_task = await crud.delete_task(task_id=task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=settings.host, port=settings.port)

