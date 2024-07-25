from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Crea una clase Item para definir los campos que se esperan en el body de la petición
class Task(BaseModel):
    _id: int = 1
    name: str
    description: str | None = None
    completed: bool = False

    def get_id(self):
        return self._id


app = FastAPI()

# CRUD para tareas.
tasks: list[Task] = []


# Create
@app.post("/task/")
async def create_task(task: Task):
    task._id = tasks[-1]._id + 1 if tasks else 1
    tasks.append(task)
    return {**task.model_dump(), "_id": task.get_id()}


# Read
@app.get("/task/")
async def read_tasks():
    return {"tasks": [{**task.model_dump(), "id": task.get_id()} for task in tasks]}


# Read by id
@app.get("/task/{task_id}")
async def read_task(task_id: int):
    for task in tasks:
        if task._id == task_id:
            return {**task.model_dump(), "id": task.get_id()}

    raise HTTPException(status_code=404, detail="Item not found")


# Update
@app.put("/task/{task_id}")
async def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t._id == task_id:
            tasks[i] = task
            task._id = task_id
            return {**task.model_dump(), "id": task.get_id()}

    raise HTTPException(status_code=404, detail="Item not found")


# Delete
@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task._id == task_id:
            tasks.pop(i)
            return {"message": f"Task deleted {task_id}"}

    raise HTTPException(status_code=404, detail="Item not found")
