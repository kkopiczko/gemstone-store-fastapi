from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel
from models.gem_models import *
import gem_repository 
from db import engine

app = FastAPI()


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


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()