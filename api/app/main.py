from fastapi import FastAPI, Body
from .models import Base, Users, Addresses, Offers, Dishes
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = "postgresql://refood:refood@my_postgres/refood_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FastAPI configuration
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Nie no": "we coś wybierz"}

@app.get("/users")
async def read_users():
    db = SessionLocal()
    users = db.query(Users).all()
    db.close()
    return users

@app.post("/users")
async def add_user(id : int = Body(), name: str = Body(), surname: str = Body(), age: int = Body(), address_id : int = Body(), phone_nr : str = Body(), rating: int = Body()):
    db = SessionLocal()
    user = Users(id=id, name=name, surname=surname, age=age, address_id=address_id, phone_nr=phone_nr, rating=rating)
    db.add(user)
    db.commit()
    db.close()

@app.get("/users/{user_id}")
async def read_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(Users).filter(Users.id == user_id).first()
    db.close()
    return user

@app.get("/addresses")
async def read_addresses():
    db = SessionLocal()
    addresses = db.query(Addresses).all()
    db.close()
    return addresses

@app.post("/addresses")
async def add_address(id : int = Body(), street_name: str = Body(), house_nr: int = Body(), apartament_nr: int = Body(), city : str = Body()):
    db = SessionLocal()
    address = Addresses(id=id, street_name=street_name, house_nr=house_nr, apartament_nr=apartament_nr, city=city)
    db.add(address)
    db.commit()
    db.close()

@app.get("/addresses/{address_id}")
async def read_address_by_id(address_id: int):
    db = SessionLocal()
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    db.close()
    return address

@app.get("/offers")
async def read_offers():
    db = SessionLocal()
    offers = db.query(Offers).all()
    db.close()
    return offers

@app.post("/offers")
async def add_offer(id : int = Body(), dish_id: int = Body(), seller_id: int = Body(), address_id: int = Body()):
    db = SessionLocal()
    offer = Offers(id=id, dish_id=dish_id, seller_id=seller_id, address_id=address_id, creation_date=current_timestamp())
    db.add(offer)
    db.commit()
    db.close()

@app.get("/offers/{offer_id}")
async def read_offer_by_id(offer_id: int):
    db = SessionLocal()
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    db.close()
    return offer

@app.get("/dishes")
async def read_dishes():
    db = SessionLocal()
    dishes = db.query(Dishes).all()
    db.close()
    return dishes

@app.post("/dishes")
async def add_dish(id : int = Body(), name : str = Body(), is_vegetarian: bool = Body(), description: str = Body(), price: int = Body(), how_many_days_before_expiration : float = Body()):
    db = SessionLocal()
    dish = Dishes(id=id, name=name, is_vegetarian=is_vegetarian, price=price, description=description, how_many_days_before_expiration=how_many_days_before_expiration)
    db.add(dish)
    db.commit()
    db.close()

@app.get("/dishes/{dish_id}")
async def read_address_by_id(dish_id: int):
    db = SessionLocal()
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    db.close()
    return dish
