from sqlalchemy import table
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import validator, EmailStr
import datetime

class User(SQLModel, table=True):
    id: Optional[str] = Field(primary_key=True)
    username: str
    password: str
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
    is_seller: bool = False

class UserCreate(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v
