# from ..main import engine
# from models.gem_models import Gem, GemProperties
# from sqlmodel import Session, select

# def select_gems():
#     with Session(bind=engine) as session:
#         statement = select(Gem)
#         statement = statement.where(Gem.id == 2)
#         result = session.exec(statement)
#         print(result.all())

# select_gems()