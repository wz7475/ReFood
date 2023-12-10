from fastapi import FastAPI, Body, HTTPException
from .models import Users, Addresses, Offers, Dishes
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .cfg import SQLALCHEMY_DATABASE_URL

# SQLAlchemy configuration

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FastAPI configuration
app = FastAPI()

@app.get("/")
async def read_root():
    return "ReFood"

@app.get("/users")
async def read_users():
    db = SessionLocal()
    users = db.query(Users).all()
    db.close()
    return users

@app.get("/users/last_id")
async def get_last_user_id():
    db = SessionLocal()
    last_id = db.query(Users.id).all()
    db.close()
    return max([row[0] for row in last_id])

@app.post("/users")
async def add_user(name: str = Body(), surname: str = Body(), age: int = Body(), address_id : int = Body(), phone_nr : str = Body(), rating: int = Body()):
    db = SessionLocal()
    user_id = await get_last_user_id() + 1
    user = Users(id=user_id, name=name, surname=surname, age=age, address_id=address_id, phone_nr=phone_nr, rating=rating)
    db.add(user)
    db.commit()
    db.close()

@app.get("/users/{user_id}")
async def read_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(Users).filter(Users.id == user_id).first()
    db.close()
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    db.close()

@app.get("/addresses")
async def read_addresses():
    db = SessionLocal()
    addresses = db.query(Addresses).all()
    db.close()
    return addresses

@app.get("/addresses/last_id")
async def get_last_address_id():
    db = SessionLocal()
    last_id = db.query(Addresses.id).all()
    db.close()
    return max([row[0] for row in last_id])

@app.post("/addresses")
async def add_address(street_name: str = Body(), house_nr: int = Body(), apartament_nr: int = Body(), city : str = Body()):
    db = SessionLocal()
    address_id = await get_last_address_id() + 1
    address = Addresses(id=address_id, street_name=street_name, house_nr=house_nr, apartament_nr=apartament_nr, city=city)
    db.add(address)
    db.commit()
    db.close()

@app.get("/addresses/{address_id}")
async def read_address_by_id(address_id: int):
    db = SessionLocal()
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    db.close()
    return address

@app.delete("/addresses/{address_id}")
async def delete_address(address_id: int):
    db = SessionLocal()
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    db.close()

@app.get("/offers")
async def read_offers():
    db = SessionLocal()
    offers = db.query(Offers).all()
    db.close()
    return offers

@app.get("/offers/last_id")
async def get_last_offer_id():
    db = SessionLocal()
    last_id = db.query(Offers.id).all()
    db.close()
    return max([row[0] for row in last_id])

@app.post("/offers")
async def add_offer(dish_id: int = Body(), seller_id: int = Body(), address_id: int = Body()):
    db = SessionLocal()
    offer_id = await get_last_offer_id() + 1
    offer = Offers(id=offer_id, dish_id=dish_id, seller_id=seller_id, address_id=address_id, creation_date=current_timestamp())
    db.add(offer)
    db.commit()
    db.close()

@app.get("/offers/{offer_id}")
async def read_offer_by_id(offer_id: int):
    db = SessionLocal()
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    db.close()
    return offer

@app.delete("/offers/{offer_id}")
async def delete_offer(offer_id: int):
    db = SessionLocal()
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(offer)
    db.commit()
    db.close()

@app.get("/dishes")
async def read_dishes():
    db = SessionLocal()
    dishes = db.query(Dishes).all()
    db.close()
    return dishes

@app.get("/dishes/last_id")
async def get_last_dish_id():
    db = SessionLocal()
    last_id = db.query(Dishes.id).all()
    db.close()
    return max([row[0] for row in last_id])

@app.post("/dishes")
async def add_dish(name : str = Body(), is_vegetarian: bool = Body(), description: str = Body(), price: int = Body(), how_many_days_before_expiration : float = Body()):
    db = SessionLocal()
    dish_id = await get_last_dish_id() + 1
    dish = Dishes(id=dish_id, name=name, is_vegetarian=is_vegetarian, price=price, description=description, how_many_days_before_expiration=how_many_days_before_expiration)
    db.add(dish)
    db.commit()
    db.close()

@app.get("/dishes/{dish_id}")
async def read_dishes_by_id(dish_id: int):
    db = SessionLocal()
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    db.close()
    return dish

@app.delete("/dishes/{dish_id}")
async def delete_dish(dish_id: int):
    db = SessionLocal()
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
    db.close()
