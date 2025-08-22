import strawberry
from database import SessionLocal
from models import User
from datetime import datetime, timedelta, timezone
from jose import jwt
import os
import uuid
import typing
from dotenv import load_dotenv
load_dotenv()
from sb_types.user import UserType
from serializers.user import to_user_type
from inputs.user import UserRegisterInput
from security import login_required, requires_permission


SECRET = os.getenv("JWT_SECRET")

@strawberry.type
class AuthPayload:
    token: str
    token_type: str = "bearer"

@strawberry.type
class UserError:
     message: str

@strawberry.type
class DeletedUserReturn:
     success: bool
     message: typing.Optional[str]
     error: typing.Optional[UserError]


def get_users() -> typing.List["UserType"]:
    with SessionLocal() as session:
        users = session.query(User).all()
        return [to_user_type(u) for u in users]
    

def register(input: "UserRegisterInput") -> "AuthPayload":
    with SessionLocal() as session:
        new_user = User(
            id=uuid.uuid4(),
            username=input.username,
            email=input.email,
            password=input.password,
            created=datetime.now(timezone.utc)
        )
        new_user.hash_password()
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return login(username=new_user.username, password=input.password)

def login(username: str, password: str) -> "AuthPayload":
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()

        if not user or not user.verify_password(password):
            return None
        
        expire = (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()
        payload = {"userid": str(user.id), "role": user.role.value, "expire": expire}
        token = jwt.encode(payload, SECRET, algorithm="HS256")
        return AuthPayload(token=token)

@login_required
def delete_user(id: str, info) -> "DeletedUserReturn":
    user = info.context["current_user"]
    with SessionLocal() as session:
        almost_deleted_user = session.query(User).filter(User.id == id).first()
        if not (almost_deleted_user.id == user["id"] or user["role"] == "admin"):
            return DeletedUserReturn(success=False, message="No rights to delete user", error="")
        
        session.delete(almost_deleted_user)
        session.commit()
        return DeletedUserReturn(success=True, message=f"user {id} was deleted", error="")
    
@requires_permission("admin")
def delete_users(ids: typing.List[str], info) -> "DeletedUserReturn":
    deleted = []
    with SessionLocal() as session:
        for id in ids:
            almost_deleted_user = session.query(User).filter(User.id == id).first()
            if almost_deleted_user:
                session.delete(almost_deleted_user)
                deleted.append(id)
        
        session.commit()
        return DeletedUserReturn(success=True, message=f"{[str(i) for i in deleted]} were deleted", error="")