from security import requires_permission
from models import UserRoles, User
from database import SessionLocal
from sb_types.user import UserType, UserRolesGQL
from serializers.user import to_user_type
from inputs.user import UserRegisterInput
import uuid
from datetime import datetime, timezone
from resolvers.user import login, AuthPayload

@requires_permission("admin")
def set_role(info, id: str, role: "UserRolesGQL") -> "UserType | None":
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            return None
        
        user.role = UserRoles(role.value)
        return to_user_type(user)
    
def spawn_boss(info, input: "UserRegisterInput") -> "AuthPayload":
    """Creates a superuser"""
    with SessionLocal() as session:
        new_boss = User(
            id=uuid.uuid4(),
            username=input.username,
            email=input.email,
            password=input.password,
            created=datetime.now(timezone.utc)
        )
        new_boss.hash_password()
        new_boss.role = UserRoles.ADMIN
        session.add(new_boss)
        session.commit()
        session.refresh(new_boss)
        return login(new_boss.username, password=input.password)