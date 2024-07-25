# Script que muestra cómo usar Pydantic para validación de datos
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Self


# ===== Encantamientos ===== #
# Define el nombre de los encantamientos
class EnchantmentNames(str, Enum):
    sharpness = "sharpness"  # Pega mas fuerte a los enemigos
    fire_aspect = "fire_aspect"  # Prende fuego a los enemigos cuando los golpeas
    knockback = "knockback"  # Empuja a los enemigos cuando los golpeas
    fortune = "fortune"  # Aumenta la cantidad de objetos que obtienes al minar, talar o desvivir enemigos


# Define la clase Enchantment para definir los campos que se esperan en el body de la petición
class Enchantment(BaseModel):
    name: EnchantmentNames
    level: int = Field(gt=0, le=4)  # Validación de un campo


# Define la clase Item para definir los campos que se esperan en el body de la petición
class Item(BaseModel):
    id: str | None = Field(default=None, validate_default=True)
    name: str
    description: str | None = None
    emerald_price: int = Field(gt=0)  # Validación de un campo
    enchantments: list[Enchantment] = []

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "diamond_sword",
                    "description": "A sword made of diamond",
                    "emerald_price": 10,
                    "enchantments": [
                        {"name": "fire_aspect", "level": 1},
                        {"name": "fortune", "level": 2},
                    ],
                }
            ]
        }
    }

    # Validaciones personalizadas sobre los campos
    @field_validator("id")
    def generate_id(cls, value: str | None):
        if value is None:
            return str(uuid4())

        raise ValueError("ID cannot be set manually")

    # Validaciones personalizadas sobre todo el modelo
    @model_validator(mode="after")
    def check_enchantments(self) -> Self:
        for enchantment in self.enchantments:
            if (
                enchantment.name == EnchantmentNames.fire_aspect
                and enchantment.level > 1
            ):
                raise ValueError(
                    "Fire Aspect enchantment cannot be higher than level 2"
                )
        return self

    # Validador de campos antes del parseo de los datos al modelo
    @model_validator(mode="before")
    def check_price(cls, data: Any) -> Any:
        if isinstance(data, dict):
            try:
                f_price = float(data.get("emerald_price", None))
            except ValueError:
                raise ValueError("Price must be a number")

            data["emerald_price"] = int(f_price)
        return data


# Lista de items
total_items: list[Item] = [
    Item(
        name="diamond_sword",
        description="A sword made of diamond",
        emerald_price=10,
        enchantments=[
            Enchantment(name=EnchantmentNames.sharpness, level=3),
            Enchantment(name=EnchantmentNames.knockback, level=2),
        ],
    ),
    Item(
        name="diamond_pickaxe",
        description="A pickaxe made of diamond",
        emerald_price=12,
        enchantments=[
            Enchantment(name=EnchantmentNames.fortune, level=3),
        ],
    ),
    Item(
        name="diamond_axe",
        description="An axe made of diamond",
        emerald_price=12,
        enchantments=[
            Enchantment(name=EnchantmentNames.sharpness, level=4),
        ],
    ),
]

app = FastAPI()


# Crear el CRUD de items
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item) -> Item:
    total_items.append(item)
    return item


@app.get("/items/", response_model=list[Item])
async def read_items(
    limit: int = Query(10, le=20)
) -> list[Item]:  # Validación de un query parameter
    return total_items[:limit]


@app.get("/items/{item_id}", response_model=Item)
async def read_item(
    item_id: str = Path(
        description="The ID of the item to get", min_length=5, max_length=50
    )
):
    for item in total_items:
        if item.id == item_id:
            return item
    return HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item: Item,
    item_id: str = Path(  # Validación de un path parameter
        description="The ID of the item to update", min_length=5, max_length=50
    ),
):
    for i, it in enumerate(total_items):
        if it.id == item_id:
            total_items[i] = item
            return item
    return HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", response_model=dict[Literal["message"], str])
async def delete_item(
    item_id: str = Path(
        description="The ID of the item to delete", min_length=5, max_length=50
    ),
):
    for i, item in enumerate(total_items):
        if item.id == item_id:
            total_items.pop(i)
            return {"message": f"Item {item_id} deleted successfully"}
    return HTTPException(status_code=404, detail="Item not found")
