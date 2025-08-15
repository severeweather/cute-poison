import strawberry
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

from datetime import datetime, timezone
import uuid

@strawberry.type
class UserType:
    id: strawberry.ID
    username: str
    created: datetime

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[UserType]:
        session: Session = SessionLocal()
        users = session.query(User).all()
        session.close()
        return [UserType(id=u.id, username=u.username, created=u.created) for u in users]
    
@strawberry.type
class Mutation:
    @strawberry.field
    def create_user(self, username: str, email: str, password: str) -> UserType:
        session: Session = SessionLocal()
        new_user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password=password,
            created=datetime.now(timezone.utc)
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()
        return UserType(id=new_user.id, username=new_user.username, created=new_user.created)
    
schema = strawberry.Schema(query=Query, mutation=Mutation)