import random
import string
from sqlmodel import Session
from main import engine
from models.gem_models import Gem, GemProperties

color_grades = string.ascii_uppercase[3:9]

clarity_variants = ['SI', 'VS', 'VVS', 'FL']

def create_gem_properties():
    size = random.randint(3, 70)/10
    color = color_grades[random.randint(0, 5)]
    clarity = clarity_variants[random.randint(0, 3)]
    gem_properties = GemProperties(size=size, color=color, clarity=clarity)
    return gem_properties

def create_gem(gem_p):
    gem = Gem(price=1000, properties_id=gem_p)
    return gem

def add_gem_to_db():
    gem_properties = create_gem_properties()
    print(gem_properties)

    with Session(bind=engine) as session:
        session.add(gem_properties)
        session.commit()
        g = create_gem(gem_properties.id)
        session.add(g)
        session.commit()

add_gem_to_db()