from fastapi import FastAPI
import uvicorn
from sqlmodel import create_engine, SQLModel
from models.gem_models import *

app = FastAPI()

engine = create_engine('sqlite:///database.db', echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get('/')
def hello():
    return "Hello there!"

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
    create_db_and_tables()