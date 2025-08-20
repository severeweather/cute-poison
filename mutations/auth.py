import strawberry
from resolvers.auth import *

@strawberry.type
class AuthMutations:
    set_role = strawberry.mutation(resolver=set_role)
    spawn_boss = strawberry.mutation(resolver=spawn_boss)