from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase): # Отображение задачи
    id: int

    class Config:
        from_attributes=True

