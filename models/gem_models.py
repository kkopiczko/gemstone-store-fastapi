from sqlalchemy import table
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

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

class Gem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    type: Optional[GemType] = GemType.DIAMOND
    properties_id: Optional[int] = Field(default=None, foreign_key='gemproperties.id')
    price: float = 1
    is_available: bool = True
    

class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float = 1
    color: Optional[GemColor] = None
    clarity: Optional[GemClarity] = None