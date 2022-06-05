from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
from sqlmodel import SQLModel, Session
from models.gem_models import *
import gem_repository 
from db import engine

app = FastAPI()

session = Session(bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get('/gems')
def get_gems():
    gems = gem_repository.select_all_gems()
    return {'gems': gems}

@app.get('/gems/{gem_id}')
def get_gem_by_id(gem_id: int):
    gem = gem_repository.select_gem_by_id(gem_id)
    return {'gem': gem}

@app.post('/gems')
def create_gem(gem_pr: GemProperties, gem: Gem):
    gem_properties = GemProperties(size=gem_pr.size, color=gem_pr.color, clarity=gem_pr.clarity)
    session.add(gem_properties)
    session.commit()
    session.refresh(gem_properties)
    gem_ = Gem(price=gem.price, type=gem.type, is_available=gem.is_available, properties_id=gem_properties.id)
    session.add(gem_)
    session.commit()
    session.refresh(gem_)
    return gem_

@app.patch('/gems/{gem_id}')
def patch_gem(gem_id: int):
    pass

@app.put('/gems/{gem_id}')
def update_gem(gem_id: int, gem: Gem):
    gem_found = session.get(Gem, gem_id)
    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    session.refresh(gem_found)
    return gem_found
    

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()