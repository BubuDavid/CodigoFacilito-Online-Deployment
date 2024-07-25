from fastapi import FastAPI

app = FastAPI()

# CONOZCAMOS LA OPENAPI DOCS (Antes Swagger)

# Lista de tareas inicial
tasks: list[str] = []


# Ruta para ver todas las tareas
@app.get("/tasks")
def read_root():
    return {"tasks": tasks}


# Ruta para ver una tarea en específico
@app.get("/tasks/{task_id}")
def read_item(task_id: int):
    # TODO: Validar que el task_id sea un número entero y que no sea mayor al tamaño de la lista, añadir el 404.
    return {"task": tasks[task_id]}


# Ruta para crear una tarea
@app.post("/tasks/create")
def create_task(task: str):
    # TODO: Validar que la tarea no esté vacía, añadir el 400.
    tasks.append(task)
    return {"task": task}


# Ruta para actualizar una tarea
@app.put("/tasks/update/{task_id}")
def update_task(task_id: int, task: str):
    # TODO: Validar que el task_id sea un número entero y que no sea mayor al tamaño de la lista, añadir el 404.
    tasks[task_id] = task
    return {"task": task}


# Ruta para eliminar una tarea
@app.delete("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    # TODO: Validar que el task_id sea un número entero y que no sea mayor al tamaño de la lista, añadir el 404.
    tasks.pop(task_id)
    return {"task_id": task_id}
