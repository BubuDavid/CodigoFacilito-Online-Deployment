# Esta no es una aplicacion de FastAPI, es un ejemplo para ver los tipos de datos en Python.

# Tipos de datos en Python
age: int = 24
name: str = "Buberto"
weight: float = 65.5
is_human: bool = True
a_byte: bytes = b"Hello, World!"

# Estrucutras de datos
## Listas
books: list[str] = ["El principito", "El arte de la guerra", "El señor de los anillos"]
califications: list[int] = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
## Tuplas
point: tuple[int, int] = (10, 20)
color: tuple[int, int, int, float] = (255, 0, 0, 0.5)
## Diccionarios
person: dict[str, int] = {"age": 24, "weight": 65}
car: dict[str, str] = {"brand": "Ford", "model": "Mustang"}
## Sets
unique_numbers: set[int] = {1, 2, 3, 4, 5}
unique_colors: set[str] = {"red", "green", "blue"}

# Tipos de datos compuestos
## Listas de tuplas
points: list[tuple[int, int]] = [(10, 20), (30, 40), (50, 60)]
## Diccionarios de listas
people: dict[str, list[str]] = {
    "names": ["Alice", "Bob", "Charlie"],
    "last_names": ["Smith", "Johnson", "Williams"],
}

# Tipos de datos opcionales
## Python 3.10
esto_es_opcional: str | None = None
## Python 3.8+
from typing import Optional, Union

esto_es_opcional: Optional[str] = None
# Esto es lo mismo que:
esto_es_opcional: Union[str, None] = None
