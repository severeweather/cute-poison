from models import Food, Nutrient, FoodNutrient
from sb_types.food import FoodType, FoodNutrientType, NutrientType

def foodnutrient_to_foodnutrient_type(foodnutrient: "FoodNutrient") -> "FoodNutrientType":
    return FoodNutrientType(
        amount=foodnutrient.amount,
        nutrient=nutrient_to_nutrient_type(foodnutrient.nutrient)
    )

def nutrient_to_nutrient_type(nutrient: "Nutrient") -> "NutrientType":
    return NutrientType(
        id=nutrient.id,
        name=nutrient.name,
        unit=nutrient.unit.value,
        created=nutrient.created,
        created_by=nutrient.created_by
    )

def food_to_food_type(food: "Food") -> "FoodType":
    return FoodType(
        id=food.id, 
        type=food.type.value, 
        name=food.name, 
        description=food.description, 
        recipe=food.recipe, 
        nutrients=[
            foodnutrient_to_foodnutrient_type(fn)
            for fn in food.nutrients
        ], 
        created=food.created,
        created_by=food.created_by
    )