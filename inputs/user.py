import strawberry

@strawberry.input
class UserRegisterInput:
    username: str
    password: str
    email: str
    