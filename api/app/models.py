import enum
import json

import bcrypt
from sqlalchemy import Column, Integer, String, Enum, Sequence, DateTime, ForeignKey, Float, select
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from .logger import get_logger

Base = declarative_base()


class Outbox(Base):
    __tablename__ = "Outbox"

    id = Column(Integer, Sequence("outbox_id_seq"), primary_key=True, index=True, autoincrement=True)
    payload = Column(String)
    routing_key = Column(String)


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    login = Column(String)
    hashed_password = Column(String)
    phone_nr = Column(String(9))

    dishes = relationship("Dishes", back_populates="author")

    offersSell = relationship("Offers", back_populates="seller", foreign_keys="[Offers.seller_id]",
                              primaryjoin="Users.id == Offers.seller_id")

    offersBuy = relationship("Offers", back_populates="buyer", foreign_keys="[Offers.buyer_id]",
                             primaryjoin="Users.id == Offers.buyer_id")

    def set_password(self, password: str):
        # Hash the password and store the hashed value
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.hashed_password = hashed_password.decode('utf-8')

    def verify_password(self, password: str) -> bool:
        # Verify the entered password against the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))


class TagsValues(enum.Enum):
    VEGETARIAN = 0
    GLUTEN_FREE = 1
    SUGAR_FREE = 2
    SHOULD_BE_EATEN_WARM = 3
    SPICY = 4


class Dishes(Base):
    __tablename__ = "Dishes"

    id = Column(Integer, Sequence("dishes_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    how_many_days_before_expiration = Column(
        Float)  # TODO w sumie nie ma sensu, powinna być data i liczone na runtime bo tak to kto zmieniejsza to, niby można od czasu wstawienia, ale nie no sus, nie podoba mi się
    author_id = Column(Integer, ForeignKey("Users.id"))
    tags = Column(MutableList.as_mutable(ARRAY(Enum(TagsValues))), nullable=True)

    author = relationship("Users", back_populates="dishes")
    dishtags = relationship("DishTags", back_populates="dishes")
    offers = relationship("Offers", back_populates="dishes")


class OfferState(enum.Enum):
    OPEN = 0
    RESERVED = 1
    COMPLETED = 2


class Offers(Base):
    __tablename__ = "Offers"

    id = Column(Integer, Sequence("offer_id_seq"), primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    state = Column(Enum(OfferState))
    dish_id = Column(Integer, ForeignKey("Dishes.id"))
    seller_id = Column(Integer, ForeignKey("Users.id"))
    buyer_id = Column(Integer, ForeignKey("Users.id"), nullable=True)
    creation_date = Column(DateTime)
    price = Column(Integer)

    seller = relationship("Users", back_populates="offersSell",
                          foreign_keys="[Offers.seller_id]", primaryjoin="Users.id == Offers.seller_id")

    buyer = relationship("Users", back_populates="offersBuy",
                         foreign_keys="[Offers.buyer_id]", primaryjoin="Users.id == Offers.buyer_id")

    dishes = relationship("Dishes", back_populates="offers")


class Tags(Base):
    __tablename__ = "Tags"

    id = Column(Integer, Sequence("tags_id_seq"), primary_key=True, autoincrement=True)
    tag = Column(Enum(TagsValues))

    dishtags = relationship("DishTags", back_populates="tags")


class DishTags(Base):
    __tablename__ = "DishTags"

    id = Column(Integer, Sequence("dishtags_id_seq"), primary_key=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey("Dishes.id"))
    tag_id = Column(Integer, ForeignKey("Tags.id"))

    dishes = relationship('Dishes', back_populates="dishtags")
    tags = relationship('Tags', back_populates="dishtags")


# utils

def read_all_offers(db, offer_id=-1):
    """
    reads current open offers

    :param db:
    :param offer_id:
    :return:
    """
    query_result = db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.seller_id == Users.id).where(Offers.state == OfferState.OPEN)
    ).all()
    return convert_offers(query_result, offer_id)


def convert_offers(query_result, offer_id=-1):
    # Convert the result to a list of dictionaries
    offers = []
    for row in query_result:
        if (int(row[8]) == int(offer_id)) or (offer_id == -1):
            offer = {
                "latitude": row[0],
                "longitude": row[1],
                "price": row[2],
                "dish_name": row[3],
                "dish_description": row[4],
                "dish_expiration_days": row[5],
                "seller_name": row[6],
                "seller_surname": row[7],
                "offer_id": row[8],
                "offer_state": row[9],
                "tags": row[10],
                "buyer_id": row[11]
            }
            offers.append(offer)
    return offers


def get_user_name(user_id, db):
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        return user.name
    return ""


def get_user_surname(user_id, db):
    user = db.query(Users).filter_by(id=user_id).first()
    if user:
        return user.surname
    return ""
