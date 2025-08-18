import strawberry
import typing
from resolvers.food import get_food_all, get_nutrients_all

@strawberry.type
class FoodQueries:
    food = strawberry.field(resolver=get_food_all)
    nutrients = strawberry.field(resolver=get_nutrients_all)