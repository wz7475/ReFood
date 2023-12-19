from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Import your defined classes
from app.models import Users, Addresses, Dishes, Offers, Base
from app.cfg import SQLALCHEMY_DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "postgresql://refood:refood@0.0.0.0/refood_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to add users
def add_users(session, num_users=5):
    for i in range(num_users):
        user = Users(
            name=f'User{i}',
            surname=f'Surname{i}',
            age=random.randint(18, 60),
            phone_nr=str(random.randint(100000000, 999999999)),
            rating=random.randint(1, 5),
            address_id=random.randint(1, 5)
        )
        session.add(user)
    session.commit()

def add_addresses(session, num_addresses=5):
    for i in range(num_addresses):
        address = Addresses(
            street_name=f'Street{i}',
            house_nr=i,
            apartament_nr=i,
            city='City' + str(i)
        )
        session.add(address)
    session.commit()


# Function to add dishes
def add_dishes(session, num_dishes=5):
    for i in range(num_dishes):
        dish = Dishes(
            name=f'Dish{i}',
            is_vegetarian=bool(random.getrandbits(1)),
            description=f'Description of Dish{i}',
            price=random.randint(10, 50),
            how_many_days_before_expiration=float(random.randint(1, 5))
        )
        session.add(dish)
    session.commit()

# Function to add offers
def add_offers(session, num_offers=10):
    for i in range(num_offers):
        offer = Offers(
            dish_id=random.randint(1, 5),
            seller_id=random.randint(1, 5),
            address_id=random.randint(1, 5),
            creation_date=datetime.now()
        )
        session.add(offer)
    session.commit()


# drop all tables
Base.metadata.drop_all(engine)

# Create tables
Base.metadata.create_all(engine)

# Add data
add_addresses(session)
add_users(session)
add_dishes(session)
add_offers(session)

# Close session
session.close()
