from sqlmodel import Session, select
from db import engine
from models.user_models import User

def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res

def get_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        res = session.exec(statement).first()
        return res

def get_user_by_id(user_id):
    with Session(engine) as session:
        res = session.get(User, user_id)
        return res