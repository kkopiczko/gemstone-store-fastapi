from fastapi import FastAPI
from routers import gems, users
import uvicorn
from sqlmodel import SQLModel
from models.gem_models import *
from models.user_models import *
from db import engine


app = FastAPI()

app.include_router(gems.router)
app.include_router(users.router)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)




if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    create_db_and_tables()