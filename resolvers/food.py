import strawberry
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Food, Nutrient, FoodNutrient
from sb_types.food import FoodNutrientType, FoodType, NutrientType
from inputs.food import *
from serializers.food import food_to_food_type, nutrient_to_nutrient_type
import typing
import uuid
from security import requires_permission

@strawberry.type
class FoodError:
     message: str

@strawberry.type
class DeletedReturn:
     success: bool
     message: typing.Optional[str]
     error: typing.Optional[FoodError]


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
    with SessionLocal() as session:
        new_nutrient = Nutrient(
            name=input.name,
            unit=input.unit,
        )
        session.add(new_nutrient)
        session.commit()
        session.refresh(new_nutrient)
        return nutrient_to_nutrient_type(new_nutrient)

def update_nutrient(id: strawberry.ID, input: "NutrientUpdateInput") -> "NutrientType | FoodError":
     with SessionLocal() as session:
          nutrient = session.query(Nutrient).filter(Nutrient.id == id).first()
          if not nutrient:
               return FoodError(message="not found")
          
          nutrient.name = input.name
          nutrient.unit = input.unit

          session.commit()
          session.refresh(nutrient)
          return nutrient_to_nutrient_type(nutrient)

def delete_nutrient(id: strawberry.ID) -> "DeletedReturn":
    with SessionLocal() as session:
          nutrient = session.query(Nutrient).filter(Nutrient.id == id).first()
          if not nutrient:
               return DeletedReturn(success=False, message="", error=FoodError(message="not found"))
          
          session.delete(nutrient)
          session.commit()
    return DeletedReturn(success=True, message=f"{id} was deleted", error=None)


def create_food(input: "FoodInput") -> "FoodType":
    with SessionLocal() as session:
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
        return food_to_food_type(new_food)

def update_food(id: strawberry.ID, input: "FoodUpdateInput") -> "FoodType | FoodError":
     with SessionLocal() as session:
          food = session.query(Food).filter(Food.id == id).first()
          if not food:
               return FoodError(message="not found")
          
          food.name = input.name  
          food.description = input.description
          food.recipe = input.recipe
          food.nutrients.clear()
          
          for n in input.nutrients:
            nutrient = session.query(Nutrient).filter(Nutrient.id == n.nutrient_id).first()
            if not nutrient:
                return FoodError(message="not found")

            food.nutrients.append(
                FoodNutrient(nutrient=nutrient, amount=n.amount)
            )
        
          session.commit()
          session.refresh(food)
          return food_to_food_type(food)
     
@requires_permission("admin")
def delete_food(id: strawberry.ID, info) -> "DeletedReturn | None":
    with SessionLocal() as session:
        food = session.query(Food).filter(Food.id == id).first()
        if not food:
             return DeletedReturn(success=False, message="", error=FoodError(message="not found"))
         
        session.delete(food)
        session.commit()
    return DeletedReturn(success=True, message=f"{id} was deleted", error=None)