from sqlmodel import create_engine, Session

engine = create_engine('sqlite:///database.db', echo=True)

session = Session(bind=engine)