from utils.jwt_manager import create_token
from schemas.user import User
from fastapi.responses import JSONResponse
from fastapi import APIRouter

user_router = APIRouter()


@user_router.post('/login', tags=['Authentication'])
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(content={'token': token}, status_code=200)
    return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)
