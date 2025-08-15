from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema

app = FastAPI()

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")