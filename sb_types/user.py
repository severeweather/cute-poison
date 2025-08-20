import strawberry
from datetime import datetime
from models import UserRoles

UserRolesGQL = strawberry.enum(UserRoles)

@strawberry.type
class UserType:
    id: strawberry.ID
    username: str
    role: "UserRolesGQL"
    created: datetime