import strawberry
from datetime import datetime
import typing

@strawberry.type
class FoodNutrientType:
    amount: float
    nutrient: "NutrientType"

@strawberry.type
class FoodType:
    id: strawberry.ID
    type: str
    name: str
    description: str
    recipe: str
    nutrients: typing.List[FoodNutrientType]
    created: datetime

@strawberry.type
class NutrientType:
    id: strawberry.ID
    name: str
    unit: str
    created: datetime
