from sqlalchemy.orm import Session
from database import SessionLocal
from models import Food, Nutrient, FoodNutrient
from sb_types.food import FoodNutrientType, FoodType, NutrientType
from inputs.food import FoodInput, NutrientInput, FoodNutrientInput
import typing
import uuid

def get_food_all() -> typing.List[FoodType]:
    session: Session = SessionLocal()
    food = session.query(Food).all()
    food_types = [
    FoodType(
        id=f.id, 
        type=f.type.value, 
        name=f.name, 
        description=f.description, 
        recipe=f.recipe, 
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
            for fn in f.nutrients
        ], 
        created=f.created
    )
    for f in food
    ]

    session.close()
    return food_types

def get_nutrients_all() -> typing.List[NutrientType]:
    session: Session = SessionLocal()
    nutrients = session.query(Nutrient).all()
    session.close()
    return [NutrientType(id=n.id, name=n.name, unit=n.unit.value, created=n.created) for n in nutrients]

def create_nutrient(input: "NutrientInput") -> "NutrientType":
        session: Session = SessionLocal()
        new_nutrient = Nutrient(
            name=input.name,
            unit=input.unit,
        )
        session.add(new_nutrient)
        session.commit()
        session.refresh(new_nutrient)
        session.close()
        return NutrientType(id=new_nutrient.id, name=new_nutrient.name, unit=new_nutrient.unit, nutrients=new_nutrient.nutrients, created=new_nutrient.created)

def create_food(input: "FoodInput") -> "FoodType":
        session: Session = SessionLocal()
        new_food = Food(
            id=uuid.uuid4(),
            type=input.type,
            name=input.name,
            description=input.description,
            recipe=input.recipe,
        )
        session.add(new_food)

        for n in input.nutrients:
            food_nutrient = FoodNutrient(
                amount=n.amount,
                nutrient_id=n.nutrient_id,
                food_id=new_food.id
            )
            session.add(food_nutrient)
        
        session.commit()
        session.refresh(new_food)

        food_type = FoodType(
            id=new_food.id,
            type=new_food.type,
            name=new_food.name,
            description=new_food.description,
            recipe=new_food.recipe,
            nutrients=[
                FoodNutrientType(
                    amount=fn.amount,
                    nutrient=NutrientType(
                        id=fn.nutrient.id,
                        name=fn.nutrient.name,
                        unit=fn.nutrient.unit,
                        created=fn.nutrient.created
                    )
                )
                for fn in new_food.nutrients
            ],
            created=new_food.created
        )

        session.close()
        return food_type