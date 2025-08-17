import strawberry
import typing
from models import FoodTypeEnum, UnitEnum

FoodTypeEnumGQL = strawberry.enum(FoodTypeEnum)
UnitEnumGQL = strawberry.enum(UnitEnum)

@strawberry.input
class FoodNutrientInput:
    amount: float
    nutrient_id: strawberry.ID

@strawberry.input
class FoodInput:
    type: FoodTypeEnumGQL
    name: str
    description: str
    recipe: str
    nutrients: typing.List[FoodNutrientInput]

@strawberry.input
class NutrientInput:
    name: str
    unit: UnitEnumGQL