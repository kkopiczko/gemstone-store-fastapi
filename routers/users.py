from fastapi import APIRouter, HTTPException, status
from auth.auth import AuthHandler
from models.user_models import UserCreate, User, UserLogin
from repos.user_repository import get_user, select_all_users
from db import session
from starlette.responses import JSONResponse
from typing import List

router = APIRouter(prefix='/users', tags=['Users'])
auth_handler = AuthHandler()

@router.get('/', response_model=List[User])
def get_all_users():
    return select_all_users()

@router.post('/register')
def register(user: UserCreate):
    user_found = get_user(user.username)
    if user_found:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with that username already exist')
    hashed_password = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, hashed_password=hashed_password, email=user.email, is_seller=False)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Registered new user")

@router.post('/login')
def login(user_credentials: UserLogin):
    user_found = get_user(user_credentials.username)
    if not user_found:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    if not auth_handler.verify_password(user_credentials.password, user_found.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = auth_handler.encode_token(user_found.id)
    return {'token': token}