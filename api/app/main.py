from fastapi import FastAPI, Body, HTTPException, Depends
from .models import Users, Addresses, Offers, Dishes
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .cfg import SQLALCHEMY_DATABASE_URL

# SQLAlchemy configuration

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
async def read_root():
    return "ReFood"

@app.get("/users")
async def read_users(db: SessionLocal = Depends(get_db)):
    users = db.query(Users).all()
    return users

@app.post("/users")
async def add_user(name: str = Body(), surname: str = Body(), age: int = Body(), address_id : int = Body(), phone_nr : str = Body(), rating: int = Body(), db: SessionLocal = Depends(get_db)):
    user_id = max([row[0] for row in db.query(Users.id).all()]) + 1
    user = Users(id=user_id, name=name, surname=surname, age=age, address_id=address_id, phone_nr=phone_nr, rating=rating)
    db.add(user)
    db.commit()

@app.get("/users/{user_id}")
async def read_user_by_id(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

@app.get("/addresses")
async def read_addresses(db: SessionLocal = Depends(get_db)):
    addresses = db.query(Addresses).all()
    return addresses

@app.post("/addresses")
async def add_address(street_name: str = Body(), house_nr: int = Body(), apartament_nr: int = Body(), city : str = Body(), db: SessionLocal = Depends(get_db)):
    address_id = max([row[0] for row in db.query(Addresses.id).all()]) + 1
    address = Addresses(id=address_id, street_name=street_name, house_nr=house_nr, apartament_nr=apartament_nr, city=city)
    db.add(address)
    db.commit()

@app.get("/addresses/{address_id}")
async def read_address_by_id(address_id: int, db: SessionLocal = Depends(get_db)):
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    return address

@app.delete("/addresses/{address_id}")
async def delete_address(address_id: int, db: SessionLocal = Depends(get_db)):
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()

@app.get("/offers")
async def read_offers(db: SessionLocal = Depends(get_db)):
    offers = db.query(Offers).all()
    return offers

@app.post("/offers")
async def add_offer(dish_id: int = Body(), seller_id: int = Body(), address_id: int = Body(), db: SessionLocal = Depends(get_db)):
    offer_id = max([row[0] for row in db.query(Offers.id).all()]) + 1
    offer = Offers(id=offer_id, dish_id=dish_id, seller_id=seller_id, address_id=address_id, creation_date=current_timestamp())
    db.add(offer)
    db.commit()

@app.get("/offers/{offer_id}")
async def read_offer_by_id(offer_id: int, db: SessionLocal = Depends(get_db)):
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    return offer

@app.delete("/offers/{offer_id}")
async def delete_offer(offer_id: int, db: SessionLocal = Depends(get_db)):
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(offer)
    db.commit()

@app.get("/dishes")
async def read_dishes(db: SessionLocal = Depends(get_db)):
    dishes = db.query(Dishes).all()
    return dishes

@app.post("/dishes")
async def add_dish(name : str = Body(), is_vegetarian: bool = Body(), description: str = Body(), price: int = Body(), how_many_days_before_expiration : float = Body(), db: SessionLocal = Depends(get_db)):
    dish_id = max([row[0] for row in db.query(Dishes.id).all()]) + 1
    dish = Dishes(id=dish_id, name=name, is_vegetarian=is_vegetarian, price=price, description=description, how_many_days_before_expiration=how_many_days_before_expiration)
    db.add(dish)
    db.commit()

@app.get("/dishes/{dish_id}")
async def read_dishes_by_id(dish_id: int, db: SessionLocal = Depends(get_db)):
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    return dish

@app.delete("/dishes/{dish_id}")
async def delete_dish(dish_id: int, db: SessionLocal = Depends(get_db)):
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
