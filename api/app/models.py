from sqlalchemy import Column, Integer, String, Boolean, Sequence, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

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
    name = Column(String)
    is_vegetarian = Column(Boolean)
    description = Column(String)
    price = Column(Integer)
    how_many_days_before_expiration = Column(Float)

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
