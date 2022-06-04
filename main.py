from fastapi import FastAPI
import uvicorn
from sqlmodel import create_engine, SQLModel
from models.gem_models import *
import gem_repository 

app = FastAPI()

engine = create_engine('sqlite:///database.db', echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get('/gems')
def get_gems():
    gems = gem_repository.select_all_gems()
    return {'gems': gems}

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()