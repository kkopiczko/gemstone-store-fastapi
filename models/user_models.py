from sqlalchemy import table
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime

class User(SQLModel, table=True):
    id: Optional[str] = Field(primary_key=True)
    username: str
    password: str
    email: str
    created_at: datetime.datetime = datetime.datetime.now()
    is_seller: bool = False

class UserCreate(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: str
