import strawberry
from resolvers.food import *

@strawberry.type
class FoodQueries:
    food = strawberry.field(resolver=get_food_all)
    food_by_id = strawberry.field(resolver=food_by_id)
    nutrients = strawberry.field(resolver=get_nutrients_all)