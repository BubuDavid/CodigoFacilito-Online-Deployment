import pickle

import numpy as np
from fastapi import FastAPI, UploadFile
from PIL import Image

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict_class_image")
def predict_class_image(file: UploadFile):
    # Cargar el modelo
    with open("03_FastAPI_ML/models/02_number_classification_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Cargar el modelo de reduccion de dimensiones
    with open("03_FastAPI_ML/models/02_number_reductor.pkl", "rb") as f:
        iso = pickle.load(f)
    image = Image.open(file.file)

    image = image.convert("L").resize((8, 8))

    image_data = np.array(image).reshape(1, -1)

    data_projected = iso.transform(image_data)

    prediction = model.predict(data_projected)

    return {"prediction": prediction.tolist()}
