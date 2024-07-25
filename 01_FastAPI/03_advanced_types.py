from enum import Enum

from fastapi import FastAPI, HTTPException

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(
    model_name: ModelName,
):  # Declarar el tipo de dato de la variable model_name
    # Check if the model_name is in the Enum
    if model_name not in ModelName:
        raise HTTPException(status_code=404, detail="Modelo no encontrado")

    # Return the model_name and a message
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "¡Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "¡LeCNN todas las imagenes!"}

    # If the model_name is resnet
    return {"model_name": model_name, "message": "Asies, soy resnet."}
