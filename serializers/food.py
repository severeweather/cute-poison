from models import Food
from sb_types.food import FoodType, FoodNutrientType, NutrientType

def food_to_food_type(food: "Food") -> "FoodType":
    return FoodType(
        id=food.id, 
        type=food.type.value, 
        name=food.name, 
        description=food.description, 
        recipe=food.recipe, 
        nutrients=[
            FoodNutrientType(
                amount=fn.amount,
                nutrient=NutrientType(
                    id=fn.nutrient.id,
                    name=fn.nutrient.name,
                    unit=fn.nutrient.unit.value,
                    created=fn.nutrient.created,
                )
            )
            for fn in food.nutrients
        ], 
        created=food.created
    )