from fastapi import FastAPI, HTTPException, Request, Body
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    address_id = Column(Integer, ForeignKey("Addresses.id"))
    phone_nr = Column(String(9))
    rating = Column(Integer)
    address = relationship("Addresses")
    

class Addresses(Base):
    __tablename__ = "Addresses"
    
    id = Column(Integer, Sequence("addresses_id_seq"), primary_key=True, index=True, autoincrement=True)
    street_name = Column(String)
    house_nr = Column(Integer)
    apartament_nr = Column(Integer)
    city = Column(String)


class Dishes(Base):
    __tablename__ = "Dishes"
    
    id = Column(Integer, Sequence("dishes_id_seq"), primary_key=True, index=True, autoincrement=True)
    is_vegetarian = Column(Boolean)
    description = Column(String)
    price = Column(Integer)
    expiration_date = Column(DateTime)

class Offers(Base):
    __tablename__ = "Offers"
    
    id = Column(Integer, Sequence("offer_id_seq"), primary_key=True, index=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey("Dishes.id"))
    seller_id = Column(Integer, ForeignKey("Users.id"))
    address_id = Column(Integer, ForeignKey("Addresses.id"))
    creation_date = Column(DateTime)
    
    address = relationship("Addresses")
    seller = relationship("Users")
    dish = relationship("Dishes")


# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URL = "postgresql://refood:refood@my_postgres/refood_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FastAPI configuration
app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Create tables
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown_event():
    # Close database connection (if needed)
    pass

@app.get("/")
def read_root():
    return {"Nie no": "we coś wybierz"}

@app.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(Users).all()
    db.close()
    return users

@app.post("/users")
def add_user(id : int = Body(), name: str = Body(), surname: str = Body(), age: int = Body(), address_id : int = Body(), phone_nr : str = Body(), rating: int = Body()):
    db = SessionLocal()
    user = Users(id=id, name=name, surname=surname, age=age, address_id=address_id, phone_nr=phone_nr, rating=rating)
    db.add(user)
    db.commit()
    db.close()

@app.get("/addresses")
def read_addresses():
    db = SessionLocal()
    addresses = db.query(Addresses).all()
    db.close()
    return addresses

@app.post("/addresses")
def add_address(id : int = Body(), street_name: str = Body(), house_nr: int = Body(), apartament_nr: int = Body(), city : str = Body()):
    db = SessionLocal()
    address = Addresses(id=id, street_name=street_name, house_nr=house_nr, apartament_nr=apartament_nr, city=city)
    db.add(address)
    db.commit()
    db.close()

@app.get("/offers")
def read_offers():
    db = SessionLocal()
    offers = db.query(Offers).all()
    db.close()
    return offers

@app.post("/offers")
def add_offer(id : int = Body(), dish_id: int = Body(), seller_id: int = Body(), address_id: int = Body(), creation_date : datetime = Body()):
    db = SessionLocal()
    offer = Offers(id=id, dish_id=dish_id, seller_id=seller_id, address_id=address_id, creation_date=creation_date)
    db.add(offer)
    db.commit()
    db.close()

@app.get("/dishes")
def read_dishes():
    db = SessionLocal()
    dishes = db.query(Dishes).all()
    db.close()
    return dishes

@app.post("/dishes")
def add_dish(id : int = Body(), is_vegetarian: bool = Body(), description: str = Body(), price: int = Body(), expiration_date : datetime = Body()):
    db = SessionLocal()
    dish = Dishes(id=id, is_vegetarian=is_vegetarian, price=price, description=description, expiration_date=expiration_date)
    db.add(dish)
    db.commit()
    db.close()

@app.get("/addresses/{address_id}")
def read_address_by_id(address_id: int):
    db = SessionLocal()
    address = db.query(Addresses).filter(Addresses.id == address_id).first()
    db.close()

    if address:
        return address
    else:
        raise HTTPException(status_code=404, detail="Address not found")
