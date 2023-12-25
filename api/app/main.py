import json
from contextlib import asynccontextmanager

import pika
from fastapi import FastAPI, Body, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from .logger import get_logger
from .models import Base, Users, Dishes, Offers, DishTags, OfferState, TagsValues, Tags
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from elasticsearch import Elasticsearch
from .cfg import SQLALCHEMY_DATABASE_URL, ADD_OFFER_QUEUE, DELETE_OFFER_QUEUE, OFFER_INDEX
from .es_tools import get_by_fulltext
from .connectors import get_rabbitmq_connection, get_es_connection
from .sessions import SessionData, backend, cookie, verifier
from uuid import UUID, uuid4
from typing import List

# SQLAlchemy configuration
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

connections = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger()
    Base.metadata.create_all(bind=engine)
    init_tag_table(SessionLocal())
    connections["logger"] = logger
    connections["add-offer"] = get_rabbitmq_connection(logger)
    connections["add-channel"] = connections["add-offer"].channel()
    connections["add-channel"].queue_declare(queue=ADD_OFFER_QUEUE)
    connections["delete-offer"] = get_rabbitmq_connection(logger)
    connections["delete-channel"] = connections["delete-offer"].channel()
    connections["delete-channel"].queue_declare(queue=DELETE_OFFER_QUEUE)
    connections["es"] = get_es_connection(logger)
    yield
    connections.clear()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test-es-add-offer/{offer_id}")
async def test_es_add_offer(offer_id: int):
    offer = {
        "id": offer_id,
        "dish_id": offer_id,
        "seller_id": offer_id,
        "address_id": offer_id,
        "creation_date": "2021-01-01",
        "description": f"test{offer_id} offer hdyż",
    }
    connections["add-channel"].basic_publish(exchange='',
                                             routing_key=ADD_OFFER_QUEUE,
                                             body=json.dumps(offer))
    return offer


@app.get("/test-es-delete-offer/{offer_id}")
async def test_es_delete_offer(offer_id: int):
    offer = {
        "id": offer_id,
    }
    connections["delete-channel"].basic_publish(exchange='',
                                                routing_key=DELETE_OFFER_QUEUE,
                                                body=json.dumps(offer))
    return offer


@app.get("/test-es-query/{pattern}")
async def test_es_query(pattern: str):
    fields = ["description"]
    result = get_by_fulltext(connections["es"], OFFER_INDEX, fields, pattern)
    return result


def init_tag_table(db: SessionLocal):
    if len(db.query(Tags).all()) == 0:
        for idx, tag_value in enumerate(
                [TagsValues.VEGETARIAN, TagsValues.GLUTEN_FREE, TagsValues.SUGAR_FREE, TagsValues.SHOULD_BE_EATEN_WARM,
                 TagsValues.SPICY]):
            tag = Tags(id=idx, tag=tag_value)
            db.add(tag)
        db.commit()


@app.get("/", dependencies=[Depends(cookie)])
async def read_root(session_data: SessionData = Depends(verifier)):
    return "ReFood"


# Sesions
@app.post("/login")
async def create_session(response: Response, login: str = Body(), password: str = Body(),
                         db: SessionLocal = Depends(get_db)):
    if db.query(Users).filter_by(login=login).first() is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    if not db.query(Users).filter_by(login=login).first().verify_password(password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    session = uuid4()
    data = SessionData(username=login)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {login}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"


@app.post("/register")
async def add_user(
        name: str = Body(),
        surname: str = Body(),
        login: str = Body(),
        password: str = Body(),
        phone_nr: str = Body(),
        db: SessionLocal = Depends(get_db)
):
    user_id = max([row[0] for row in db.query(Users.id).all()] + [-1]) + 1  # TODO switch to autoincrement in future pls
    if db.query(Users).filter_by(login=login).first() is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    user = Users(
        id=user_id,
        name=name,
        surname=surname,
        login=login,
        phone_nr=phone_nr
    )
    user.set_password(password)
    db.add(user)
    db.commit()
    return f"user {login} created"


@app.delete("/users", dependencies=[Depends(cookie)])
async def delete_user(session_data: SessionData = Depends(verifier), db: SessionLocal = Depends(get_db)):
    user = db.query(Users).filter(Users.login == session_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


@app.get("/offers", dependencies=[Depends(cookie)])
async def read_offers(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    offers = db.execute(
        select(Offers.c["latitude", "longitude", "price"], Dishes.c["name", "description", "price", "how_many_days_before_expiration"], Users.c["name", "surname"]).join(Dishes).join(Offers.seller_id).where(Offers.state == 0)
    )
    return offers


@app.post("/offers", dependencies=[Depends(cookie)])
async def add_offer(
        latitude: float = Body(),
        longitude: float = Body(),
        dish_name: str = Body(),
        description: str = Body(),
        price: int = Body(),  # price in grosze
        how_many_days_before_expiration: float = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    offer_id = max([row[0] for row in db.query(Offers.id).all()] + [-1]) + 1
    user_id = db.query(Users).filter_by(login=session_data.username).first().id

    dish_id = max([row[0] for row in db.query(Dishes.id).all()] + [-1]) + 1
    dish = Dishes(
        id=dish_id,
        name=dish_name,
        price=price,
        description=description,
        how_many_days_before_expiration=how_many_days_before_expiration,
        author_id=user_id
    )
    db.add(dish)

    offer = Offers(
        id=offer_id,
        dish_id=dish_id,
        latitude=latitude,
        longitude=longitude,
        state=OfferState.OPEN,
        seller_id=user_id,
        creation_date=current_timestamp()
    )
    db.add(offer)
    db.commit()
    return offer_id


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


@app.post("/dishes", dependencies=[Depends(cookie)])
async def add_dish(
        name: str = Body(),
        description: str = Body(),
        price: int = Body(),
        how_many_days_before_expiration: float = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    dish_id = max([row[0] for row in db.query(Dishes.id).all()] + [-1]) + 1
    dish = Dishes(
        id=dish_id,
        name=name,
        price=price,
        description=description,
        how_many_days_before_expiration=how_many_days_before_expiration,
        author_id=user_id
    )
    db.add(dish)
    db.commit()
    return dish_id


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


@app.get("/dishtags")
async def read_dishtags(db: SessionLocal = Depends(get_db)):
    dishtags = db.query(DishTags).all()
    return dishtags


@app.post("/dishtags")
async def add_dishtag(
        dish_id: int = Body(),
        tag_id: int = Body(),
        db: SessionLocal = Depends(get_db)
):
    dishtag_id = max([row[0] for row in db.query(DishTags.id).all()] + [-1]) + 1
    dishtag = Dishes(
        id=dishtag_id,
        dish_id=dish_id,
        tag_id=tag_id
    )
    db.add(dishtag)
    db.commit()
    return dishtag_id


@app.get("/dishtags/{dishtag_id}")
async def read_dishtag_by_id(dishtag_id: int, db: SessionLocal = Depends(get_db)):
    dishtag = db.query(DishTags).filter(DishTags.id == dishtag_id).first()
    return dishtag


@app.delete("/dishtags/{dishtags_id}")
async def delete_dishtag(dishtag_id: int, db: SessionLocal = Depends(get_db)):
    dishtag = db.query(DishTags).filter(DishTags.id == dishtag_id).first()
    if not dishtag:
        raise HTTPException(status_code=404, detail="DishTag not found")
    db.delete(dishtag)
    db.commit()


@app.get("/get_tags_map")
async def get_tags_map():
    return {
        0: "vege",
        1: "glutenFree",
        2: "sugarFree",
        3: "shouldBeWarm",
        4: "spicy"
    }


@app.post("/add_tags_to_dish")
async def add_tags_to_dish(dish_id: int, list_of_tag_id: list[int]):
    for tag_id in list_of_tag_id:
        add_dishtag(dish_id, tag_id)


@app.post("/add_full_offer")
async def add_offer_full(
        latitude: float = Body(),
        longitude: float = Body(),
        seller_id: int = Body(),  # get user id from session
        name: str = Body(),
        description: str = Body(),
        price: int = Body(),
        how_many_days_before_expiration: float = Body(),
        list_of_tag_id: list[int] = Body(),
        db: SessionLocal = Depends(get_db)
):
    dish_id = add_dish(name, description, price, how_many_days_before_expiration)
    add_tags_to_dish(dish_id, list_of_tag_id)
    offer_id = add_offer(latitude, longitude, dish_id, seller_id)
    return offer_id
