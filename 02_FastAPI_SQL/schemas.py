from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
