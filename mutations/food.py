import strawberry
from resolvers.food import create_food, create_nutrient

@strawberry.type
class FoodMutations:
    create_food = strawberry.mutation(resolver=create_food)
    # update_food = strawberry.mutation(resolver=update_food)
    # delete_food = strawberry.mutation(resolver=delete_food)

    create_nutrient = strawberry.mutation(resolver=create_nutrient)
    # update_nutrient = strawberry.mutation(resolver=update_nutrient)
    # delete_nutrient = strawberry.mutation(resolver=delete_nutrient)