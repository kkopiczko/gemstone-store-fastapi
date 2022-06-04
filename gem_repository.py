from main import engine
from models.gem_models import Gem, GemProperties
from sqlmodel import Session, select

def select_all_gems():
    with Session(bind=engine) as session:
        statement = select(Gem, GemProperties).where(Gem.properties_id == GemProperties.id)
        # statement = statement.where(Gem.id == 2)
        result = session.exec(statement)
        # print(result.all())
        return result.all()

def select_gem_by_id(gem_id):
    with Session(bind=engine) as session:
        statement = select(Gem, GemProperties).where(Gem.properties_id == GemProperties.id)
        statement = statement.where(Gem.id == gem_id)
        result = session.exec(statement)
        return result.one()