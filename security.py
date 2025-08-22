from passlib.context import CryptContext
from functools import wraps
from graphql import GraphQLError
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def requires_permission(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            info = kwargs.get("info") or (args[0] if args else None)
            if not info:
                raise GraphQLError("Unauthorized")
            
            user = info.context.get("user")
            if not user:
                raise GraphQLError("Internal Error: User missing")
            
            if datetime.now(timezone.utc).timestamp() > user.get("expire"):
                raise GraphQLError("Token expired")

            if not user.get("role") == role:
                raise GraphQLError("Unauthorized")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = kwargs.get("info") or (args[0] if args else None)
        if not info:
            raise GraphQLError("Unauthorized")
        
        user = info.context.get("user")
        if not user:
            raise GraphQLError("Internal Error: User missing")
        
        info.context["current_user"] = user
        return func(*args, **kwargs)
    return wrapper


def ownership_required(subject, object):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not str(subject["id"]) == str(object.created_by) or str(subject["role"]) == "admin":
                raise GraphQLError(f"Ownership mismatch {subject['id']} {object.created_by}")
            return func(*args, **kwargs)
        return wrapper
    return decorator