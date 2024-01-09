import enum

from sqlalchemy import Column, Integer, Enum, Sequence, DateTime, ForeignKey, Float, String, select
from sqlalchemy.orm import relationship
from .dishes import Dishes
from .users import Users, get_user_name, get_user_surname
from .shered import Base
from sqlalchemy.sql.functions import current_timestamp
import json
from ..utils.cfg import ADD_OFFER_QUEUE


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


class Outbox(Base):
    __tablename__ = "Outbox"

    id = Column(Integer, Sequence("outbox_id_seq"), primary_key=True, index=True, autoincrement=True)
    payload = Column(String)
    routing_key = Column(String)
    status = Column(String)


# utils

def read_open_offers_by_offer_id(db, offer_id):
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
        .join_from(Offers, Users, Offers.seller_id == Users.id).where((Offers.state == OfferState.OPEN) & (Offers.id == offer_id))
    ).all()
    return query_result


def read_all_open_offers(db):
    """
    reads current open offers

    :param db:
    :param offer_id:
    :return:
    """
    query_result = db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state,
               Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.seller_id == Users.id).where(Offers.state == OfferState.OPEN)
    ).all()
    return query_result


def read_all_offers(db):
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
        .join_from(Offers, Users, Offers.seller_id == Users.id)
    ).all()
    return query_result


def convert_offers(query_result, offer_id=-1):
    # Convert the result to a list of dictionaries
    offers = []
    if query_result is None:
        return offers
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


def read_sold_offers(user_id, db):
    return db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.seller_id == Users.id)
        .filter_by(id=user_id)
    )


def read_bought_offers(user_id, db):
    return db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.buyer_id == Users.id)
        .filter_by(id=user_id)
    )


def add_users(offer, selling, db):
    buyer_id = offer["buyer_id"]
    offer["buyer_name"] = get_user_name(buyer_id, db)
    offer["buyer_surname"] = get_user_surname(buyer_id, db)
    offer["selling"] = selling
    offer["buying"] = not selling
    return offer


def get_offer_es(db, offer: Offers):
    dish = db.query(Dishes).filter_by(id=offer.dish_id).first()
    if dish:
        return {
            "id": offer.id,
            "dish_name": dish.name,
            "description": dish.description,
            "tags": [x.value for x in dish.tags],
            "location": {
                "lat": offer.latitude,
                "lon": offer.longitude
            }
        }
    return {
        "id": offer.id,
        "dish_name": "",
        "description": "",
        "tags": [],
        "location":
            {
                "lat": 0,
                "lon": 0
            }
    }


def get_index_outbox(db, offer):
    return Outbox(
        payload=json.dumps(get_offer_es(db, offer)),
        routing_key=ADD_OFFER_QUEUE,
        status="pending"
    )


def add_offer_db(db, dish_id, latitude, longitude, price, user_id):
    offer_id = max([row[0] for row in db.query(Offers.id).all()] + [-1]) + 1
    offer = Offers(
        id=offer_id,
        dish_id=dish_id,
        latitude=latitude,
        longitude=longitude,
        state=OfferState.OPEN,
        price=price,
        seller_id=user_id,
        creation_date=current_timestamp()
    )
    db.add(offer)
    db.add(get_index_outbox(db, offer))
    db.commit()  # offer and indexing_outbox have to be in one transaction
    return offer_id


def change_offer_state(db, offer_id, user_id, state):
    offer = db.query(Offers).filter_by(id=offer_id).first()
    if offer is None:
        return False
    offer.buyer_id = user_id
    offer.state = state
    db.commit()
    return True

