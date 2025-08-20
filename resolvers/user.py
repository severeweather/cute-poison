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


SECRET = os.getenv("JWT_SECRET")

def get_users() -> typing.List["UserType"]:
    with SessionLocal() as session:
        users = session.query(User).all()
        return [to_user_type(u) for u in users]

@strawberry.type
class AuthPayload:
    token: str
    token_type: str = "bearer"

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
        
        expire = (datetime.now(timezone.utc) + timedelta(minutes=1)).timestamp()
        payload = {"userid": str(user.id), "role": user.role.value, "expire": expire}
        token = jwt.encode(payload, SECRET, algorithm="HS256")
        return AuthPayload(token=token)

# def logout()