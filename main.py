from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import graphql_app

app = FastAPI()

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")