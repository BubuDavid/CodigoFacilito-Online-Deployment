import os
from uuid import uuid4

import cv2
import cvlib as cv
import numpy as np
from cvlib.object_detection import draw_bbox
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response

dir_name = "./images_uploaded"
os.makedirs(dir_name, exist_ok=True)

app = FastAPI(title="¡Puedo tener metadata también!")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
async def predict(file: UploadFile):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=415, detail="Unsupported media type")
    # Leer la imagen
    contents: bytes = await file.read()

    # Convertir la imagen a un array de numpy
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

    # Detectar los objetos
    bbox, label, conf = cv.detect_common_objects(
        image,
        model="yolov3-tiny",
    )

    # Dibujar los bounding boxes
    output_image = draw_bbox(image, bbox, label, conf)

    # Guardar la imagen
    image_path = f"{dir_name}/{uuid4()}-{file.filename}"

    cv2.imwrite(image_path, output_image)

    with open(image_path, "rb") as file_image:
        return Response(content=file_image.read(), media_type="image/jpeg")
