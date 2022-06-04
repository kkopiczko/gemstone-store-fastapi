import random
import string
from sqlmodel import Session
from main import engine
from models.gem_models import Gem, GemProperties

color_multiplier = {
    'D': 1.8,
    'E': 1.6,
    'G': 1.4,
    'F': 1.2,
    'H': 1,
    'I': 0.8
}

def calculate_gem_price(gem: Gem, gem_pr: GemProperties):
    price = 1000
    if gem.type == 'RUBY':
        price = 400
    elif gem.type == 'EMERALD':
        price = 650

    if gem_pr.clarity == 'SI':
        price *= 0.75
    elif gem_pr.clarity == 'VVS':
        price *= 1.25
    elif gem_pr.clarity == 'FL':
        price *= 1.5

    price = price * (gem_pr.size**3)

    if gem.gem_type == 'DIAMOND':
        multiplier = color_multiplier[gem_pr.color]
        price *= multiplier
    
    return price


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