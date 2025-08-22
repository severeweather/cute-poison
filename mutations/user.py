import strawberry
from resolvers.user import *

@strawberry.type
class UserMutations:
    register = strawberry.mutation(resolver=register)
    login = strawberry.mutation(resolver=login)
    delete_user = strawberry.mutation(resolver=delete_user)
    delete_users = strawberry.mutation(resolver=delete_users)