from dotenv import load_dotenv
load_dotenv()
import os
import strawberry
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal
from fastapi import Request
from jose import jwt, JWTError
from strawberry.fastapi import GraphQLRouter
from queries.food import FoodQueries
from queries.user import UserQueries
from mutations.food import FoodMutations
from mutations.user import UserMutations
from mutations.auth import AuthMutations


SECRET = os.getenv("JWT_SECRET")
    
def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return {"id": payload["userid"], "role": payload["role"], "expire": payload["expire"]}
    except JWTError:
        return None

async def get_context(request: Request):
    user = get_current_user(request)
    return {"user": user}


@strawberry.type
class Query(FoodQueries, UserQueries):
    pass
    
@strawberry.type
class Mutation(FoodMutations, UserMutations, AuthMutations):
    pass

    
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)