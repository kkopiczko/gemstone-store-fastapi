import random
import string
from sqlmodel import Session
from db import engine
from models.gem_models import Gem, GemClarity, GemColor, GemProperties, GemType

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

    if gem.type == 'DIAMOND':
        multiplier = color_multiplier[gem_pr.color]
        price *= multiplier
    
    return price


def create_gem_properties():
    size = random.randint(3, 70)/10
    color = random.choice(GemColor.list())
    clarity = random.choice(GemClarity.list())
    gem_properties = GemProperties(size=size, color=color, clarity=clarity)
    return gem_properties

def create_gem(gem_p):
    type = random.choice(GemType.list())
    gem = Gem(price=1000, properties_id=gem_p.id, type=type)
    price = calculate_gem_price(gem, gem_p)
    gem.price = round(price, 2)
    return gem

def add_gem_to_db():
    gem_properties = [create_gem_properties() for x in range(100)]
    print(gem_properties)

    with Session(bind=engine) as session:
        session.add_all(gem_properties)
        session.commit()
        gems = [create_gem(gem_properties[x]) for x in range(100)]
        session.add_all(gems)
        session.commit()

# add_gem_to_db()