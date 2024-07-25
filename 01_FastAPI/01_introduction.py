# Importa la clase FastAPI del modulo fastapi
from fastapi import FastAPI

# Crea una instancia del objeto FastAPI y la almacena en la variable app
app = FastAPI()

# Rutas: Usadas para definir las URL's a las que se puede acceder
@app.get("/") # Define una ruta en la raiz de la aplicacion
async def read_root(): # Define una funcion que retorna un diccionario
    return {"Hello": "World"}


@app.get("/about-me") # Define una ruta con el path /about-me
async def about_me(): # Funcion con una logica que retorna un diccionario (FastAPI lo convierte a JSON automaticamente)
    return {"name": "Jorge", "age": 25, "country": "Mexico"}
