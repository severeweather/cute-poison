import strawberry
from database import SessionLocal
from models import Food, Nutrient, FoodNutrient
from sb_types.food import FoodType, NutrientType
from inputs.food import *
from serializers.food import food_to_food_type, nutrient_to_nutrient_type
import typing
import uuid
from security import requires_permission, login_required, ownership_required

@strawberry.type
class FoodError:
     message: str

@strawberry.type
class DeletedReturn:
     success: bool
     message: typing.Optional[str]
     error: typing.Optional[FoodError]
     

def get_food_all(info) -> typing.List[FoodType]:
    with SessionLocal() as session:
        food = session.query(Food).all()
        return [food_to_food_type(f) for f in food]
    
def food_by_id(id: str, info) -> "FoodType | FoodError":
    with SessionLocal() as session:
        food = session.query(Food).filter(Food.id == id).first()
        if not food:
            return FoodError(message=f"{id} not found")
        return food_to_food_type(food)

def get_nutrients_all(info) -> typing.List[NutrientType]:
    with SessionLocal() as session:
        nutrients = session.query(Nutrient).all()
        return [nutrient_to_nutrient_type(n) for n in nutrients]


@requires_permission("admin")
def create_nutrient(input: "NutrientInput", info) -> "NutrientType":
    with SessionLocal() as session:
        new_nutrient = Nutrient(
            name=input.name,
            unit=input.unit,
        )
        session.add(new_nutrient)
        session.commit()
        session.refresh(new_nutrient)
        return nutrient_to_nutrient_type(new_nutrient)

@requires_permission("admin")
def update_nutrient(id: strawberry.ID, input: "NutrientUpdateInput", info) -> "NutrientType | FoodError":
     with SessionLocal() as session:
          nutrient = session.query(Nutrient).filter(Nutrient.id == id).first()
          if not nutrient:
               return FoodError(message="not found")
          
          nutrient.name = input.name
          nutrient.unit = input.unit

          session.commit()
          session.refresh(nutrient)
          return nutrient_to_nutrient_type(nutrient)

@requires_permission("admin")
def delete_nutrient(id: strawberry.ID, info) -> "DeletedReturn":
    with SessionLocal() as session:
        nutrient = session.query(Nutrient).filter(Nutrient.id == id).first()
        if not nutrient:
              return DeletedReturn(success=False, message="", error=FoodError(message="not found"))
                    
        session.delete(nutrient)
        session.commit()
        return DeletedReturn(success=True, message=f"{id} was deleted", error=None)


@login_required
def create_food(input: "FoodInput", info) -> "FoodType":
    user = info.context["current_user"]
    with SessionLocal() as session:
        new_food = Food(
            id=uuid.uuid4(),
            type=input.type,
            name=input.name,
            description=input.description,
            recipe=input.recipe,
            created_by=user["id"]
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

@login_required
def update_food(id: strawberry.ID, input: "FoodUpdateInput", info) -> "FoodType | FoodError":
    user = info.context["current_user"]
    with SessionLocal() as session:
        food = session.query(Food).filter(Food.id == id).first()
        if not food:
               return FoodError(message="not found")
          
        @ownership_required(user, food)
        def apply_updates():
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
            
        apply_updates()
        session.commit()
        session.refresh(food)
        return food_to_food_type(food)
     
@login_required
def delete_food(id: strawberry.ID, info) -> "DeletedReturn":
    user = info.context["current_user"]
    with SessionLocal() as session:
        food = session.query(Food).filter(Food.id == id).first()
        if not food:
             return DeletedReturn(success=False, message="", error=FoodError(message="not found"))
        
        @ownership_required(user, food)
        def perform_deletion():
            session.delete(food)
        
        perform_deletion()
        session.commit() 
        return DeletedReturn(success=True, message=f"{id} was deleted", error=None)