from fastapi import APIRouter, HTTPException, status
from auth.auth import AuthHandler
from models.user_models import UserCreate, User
from repos.user_repository import get_user
from db import session
from starlette.responses import JSONResponse

router = APIRouter(prefix='/users', tags=['Users'])
auth_handler = AuthHandler()

@router.post('/register')
def register(user: UserCreate):
    # user_found = get_user(user.username)
    # if user_found:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with that username already exist')
    hashed_password = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, hashed_password=hashed_password, email=user.email, is_seller=False)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Registered new user")