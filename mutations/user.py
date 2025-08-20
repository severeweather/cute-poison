import strawberry
from resolvers.user import *

@strawberry.type
class UserMutations:
    register = strawberry.mutation(resolver=register)
    login = strawberry.mutation(resolver=login)
    # logout = strawberry.mutation(resolver=logout)