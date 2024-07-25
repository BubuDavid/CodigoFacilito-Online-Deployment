import os
import pickle
from uuid import uuid4

import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Manera tranquila de enviar punto y recibir la clasificacion
@app.get("/predict_class")
def predict_class(
    x: float = Query(..., description="The x value", ge=-5, le=7),
    y: float = Query(..., description="The y value", ge=-13, le=4),
):
    with open("03_FastAPI_ML/models/01_simple_model.pkl", "rb") as f:
        model = pickle.load(f)

    new_data = np.array([[x, y]])

    model.predict(new_data)

    return {"prediction": model.predict(new_data).tolist()}


# Manera mas perrilla de enviar punto y recibir la clasificacion
class Point(BaseModel):
    x: float = Field(..., description="The x value", ge=-5, le=7)
    y: float = Field(..., description="The y value", ge=-13, le=4)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"x": 2, "y": -12},
            ]
        }
    }

    def to_numpy(self):
        return np.array([self.x, self.y]).reshape(1, -1)


# Ten cuidado al enviar imagenes asi
@app.post("/predict_class_image", response_class=FileResponse)
async def predict_class_image(point: Point):
    with open("03_FastAPI_ML/models/01_simple_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Generar la figura
    _, ax = plt.subplots()

    # Dummy data
    rng = np.random.RandomState(0)
    X = np.array([-6, -14]) + np.array([14, 18]) * rng.rand(20000, 2)
    y = model.predict(X)

    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap="RdBu", alpha=0.5)
    ax.scatter(point.x, point.y, s=100, c="#FFDE4D")

    # Guardar la figura
    os.makedirs("03_FastAPI_ML/images", exist_ok=True)
    name = uuid4()
    plot_filename = f"03_FastAPI_ML/images/{name}.png"
    plt.savefig(plot_filename)
    plt.close()

    return FileResponse(plot_filename, media_type="image/png")
