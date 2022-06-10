# from sqlalchemy import table
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum as Enum_
from typing import Optional
from models.user_models import User

class Enum(Enum_):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class GemClarity(str, Enum):
    SI = 'SI'
    VS = 'VS'
    VVS = 'VVS'
    FL = 'FL'

class GemColor(str, Enum):
    D = 'D'
    E = 'E'
    G = 'G'
    F = 'F'
    H = 'H'
    I = 'I'

class GemType(str, Enum):
    DIAMOND = 'DIAMOND'
    EMERALD = 'EMERALD'
    RUBY = 'RUBY'

class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    color: Optional[GemColor] = None
    clarity: Optional[GemClarity] = None
    gem: Optional['Gem'] = Relationship(back_populates='properties')

class Gem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    type: Optional[GemType] = GemType.DIAMOND
    price: float = 1000 
    is_available: bool = True
    properties_id: Optional[int] = Field(default=None, foreign_key='gemproperties.id')
    properties: Optional[GemProperties] = Relationship(back_populates='gem')
    seller_id: Optional[int] = Field(default=None, foreign_key='user.id')
    seller: Optional[User] = Relationship()
    
class GemPatch(SQLModel):
    price:  Optional[float]
    is_available:  Optional[bool] = True
    type:  Optional[GemType] = GemType.DIAMOND

    properties_id: Optional[int] = Field(default=None, foreign_key='gemproperties.id')
    properties: Optional[GemProperties] = Relationship(back_populates='gem') 
