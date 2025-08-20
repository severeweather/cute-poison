from sb_types.user import UserType
from models import User

def to_user_type(user: "User") -> "UserType":
    return UserType(
        id=user.id,
        username=user.username,
        role=user.role,
        created=user.created
    )