from fastapi import FastAPI
from routers import gems, users
import uvicorn
# from sqlmodel import SQLModel, Session
from models.gem_models import *


app = FastAPI()

app.include_router(gems.router)
app.include_router(users.router)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)




if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    # create_db_and_tables()