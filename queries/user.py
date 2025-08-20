import strawberry
from sb_types.user import UserType
from resolvers.user import get_users

@strawberry.type
class UserQueries:
    get_users = strawberry.field(resolver=get_users)