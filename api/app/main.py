import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, HTTPException, Depends, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from .logger import get_logger
from .models import Base, Users, Dishes, Offers, OfferState, TagsValues, Tags, read_all_offers, \
    convert_offers, get_user_name, get_user_surname, Outbox
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import select
from .cfg import ADD_OFFER_QUEUE, DELETE_OFFER_QUEUE, OFFER_INDEX
from .es_tools import get_by_fulltext
from .connectors import get_rabbitmq_connection, get_es_connection
from .sessions import SessionData, backend, cookie, verifier
from .backgroundtasks import send_messages_from_outbox
from uuid import UUID, uuid4

from .sqlalchemy import engine, SessionLocal, get_db

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
    offers = read_all_offers(db)
    return offers


@app.get("/offers_filter/{pattern}", dependencies=[Depends(cookie)])
async def read_offers(pattern: str, db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    fields = ["description", "dish_name"]
    result = get_by_fulltext(connections["es"], OFFER_INDEX, fields, pattern)
    hits = result["hits"]["hits"]
    offers = []
    for hit in hits:
        cur_offers = read_all_offers(db, hit["_id"])
        if len(cur_offers) > 0:
            offers.append(cur_offers[0])
    return offers


@app.get("/my_offers", dependencies=[Depends(cookie)])
async def read_offers(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    # TODO add buyer name and surname to samo w offer by id
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    sell_query_result = db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.seller_id == Users.id)
        .filter_by(id=user_id)
    )
    sell_offers = convert_offers(sell_query_result)
    buy_query_result = db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.buyer_id == Users.id)
        .filter_by(id=user_id)
    )
    buy_offers = convert_offers(buy_query_result)
    offers = []
    for offer in sell_offers:
        buyer_id = offer["buyer_id"]
        offer["buyer_name"] = get_user_name(buyer_id, db)
        offer["buyer_surname"] = get_user_surname(buyer_id, db)
        offer["selling"] = True
        offer["buying"] = False
        offers.append(offer)
    for offer in buy_offers:
        buyer_id = offer["buyer_id"]
        offer["buyer_name"] = get_user_name(buyer_id, db)
        offer["buyer_surname"] = get_user_surname(buyer_id, db)
        offer["selling"] = False
        offer["buying"] = True
        offers.append(offer)
    return offers


@app.post("/offers", dependencies=[Depends(cookie)])
async def add_offer(
        background_tasks: BackgroundTasks,
        latitude: float = Body(),
        longitude: float = Body(),
        dish_name: str = Body(),
        description: str = Body(),
        price: int = Body(),  # price in grosze
        how_many_days_before_expiration: float = Body(),
        tags: list[int] = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    offer_id = max([row[0] for row in db.query(Offers.id).all()] + [-1]) + 1
    user = db.query(Users).filter_by(login=session_data.username).first()

    dish_id = max([row[0] for row in db.query(Dishes.id).all()] + [-1]) + 1

    enum_tags = []
    for tag_val in tags:
        enum_tags.append(TagsValues(tag_val))

    dish = Dishes(
        id=dish_id,
        name=dish_name,
        description=description,
        how_many_days_before_expiration=how_many_days_before_expiration,
        author_id=user.id,
        tags=enum_tags
    )
    db.add(dish)

    offer = Offers(
        id=offer_id,
        dish_id=dish_id,
        latitude=latitude,
        longitude=longitude,
        state=OfferState.OPEN,
        price=price,
        seller_id=user.id,
        creation_date=current_timestamp()
    )
    offer_es = {
        "id": offer_id,
        "dish_name": dish_name,
        "description": description,
    }

    indexing_outbox = Outbox(
        payload=json.dumps(offer_es),
        routing_key=ADD_OFFER_QUEUE,
        status="pending"
    )
    db.add(offer)
    db.add(indexing_outbox)
    db.commit()  # offer and indexing_outbox have to be in one transaction
    # TODO add background task to add offer to elastic search
    background_tasks.add_task(send_messages_from_outbox, connections["add-channel"], connections["logger"])
    return offer_id


@app.post("/offers_dish", dependencies=[Depends(cookie)])
async def add_offer(
        dish_id: int = Body(),
        latitude: float = Body(),
        longitude: float = Body(),
        price: int = Body(),  # price in grosze
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    offer_id = max([row[0] for row in db.query(Offers.id).all()] + [-1]) + 1
    user_id = db.query(Users).filter_by(login=session_data.username).first().id

    # valid if dish exists
    if not db.query(Dishes).filter(Dishes.id == dish_id).first():
        raise HTTPException(status_code=404, detail="Dish not found")

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
    db.commit()
    return offer_id


@app.get("/offers/{offer_id}", dependencies=[Depends(cookie)])
async def read_offer_by_id(offer_id: int, db: SessionLocal = Depends(get_db),
                           session_data: SessionData = Depends(verifier)):
    query_result = db.execute(
        select(Offers.latitude, Offers.longitude, Offers.price, Dishes.name, Dishes.description,
               Dishes.how_many_days_before_expiration, Users.name, Users.surname, Offers.id, Offers.state, Dishes.tags,
               Offers.buyer_id)
        .join_from(Offers, Dishes, Offers.dish_id == Dishes.id)
        .join_from(Offers, Users, Offers.seller_id == Users.id)).all()
    offers = convert_offers(query_result, offer_id)
    rdy_offers = []
    for offer in offers:
        buyer_id = offer["buyer_id"]
        offer["buyer_name"] = get_user_name(buyer_id, db)
        offer["buyer_surname"] = get_user_surname(buyer_id, db)
        rdy_offers.append(offer)
    if len(offers) == 0:
        raise HTTPException(status_code=404, detail="Offer not found")
    return rdy_offers


@app.delete("/offers/{offer_id}", dependencies=[Depends(cookie)])
async def delete_offer(offer_id: int, background_tasks: BackgroundTasks, db: SessionLocal = Depends(get_db),
                       session_data: SessionData = Depends(verifier)):
    offer = db.query(Offers).filter(Offers.id == offer_id).first()
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if offer.seller_id != user_id:
        raise HTTPException(status_code=403, detail="Can not delete not yours offer")

    indexing_outbox = Outbox(
        payload=json.dumps({"id": offer_id}),
        routing_key=DELETE_OFFER_QUEUE,
        status="pending"
    )

    db.add(indexing_outbox)
    db.delete(offer)
    db.commit()
    background_tasks.add_task(send_messages_from_outbox, connections["delete-channel"], connections["logger"])


@app.get("/my_dishes", dependencies=[Depends(cookie)])
async def read_dishes(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    dishes = db.query(Dishes).filter_by(author_id=int(user_id)).all()
    return dishes


@app.get("/dishes/{dish_id}", dependencies=[Depends(cookie)])
async def read_dishes_by_id(dish_id: int, db: SessionLocal = Depends(get_db),
                            session_data: SessionData = Depends(verifier)):
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    dish = db.query(Dishes).filter(Dishes.id == dish_id).filter_by(author_id=int(user_id)).all()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@app.delete("/dishes/{dish_id}")
async def delete_dish(dish_id: int, db: SessionLocal = Depends(get_db)):
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()


@app.post("/dishes", dependencies=[Depends(cookie)])
async def add_dish(
        name: str = Body(),
        description: str = Body(),
        how_many_days_before_expiration: float = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    dish_id = max([row[0] for row in db.query(Dishes.id).all()] + [-1]) + 1
    dish = Dishes(
        id=dish_id,
        name=name,
        description=description,
        how_many_days_before_expiration=how_many_days_before_expiration,
        author_id=user_id
    )
    db.add(dish)
    db.commit()
    return dish_id


@app.get("/complete_offer/{offer_id}", dependencies=[Depends(cookie)])
async def complete_offer(
        offer_id: int,
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user_id = db.query(Users).filter_by(login=session_data.username).first().id
    offer = db.query(Offers).filter_by(id=offer_id).first()
    if offer is None:
        HTTPException(status_code=404, detail="Offer not found")
    offer.buyer_id = user_id
    offer.state = OfferState.COMPLETED
    db.commit()
    return "ok"


@app.post("/reserve_offer", dependencies=[Depends(cookie)])
async def reserve_offer(
        offer_id: int = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    offer = db.query(Offers).filter_by(id=offer_id).first()
    if offer is None:
        HTTPException(status_code=404, detail="Offer not found")
    offer.state = OfferState.RESERVED
    db.commit()
    return "ok"


# @app.get("/dishtags")
# async def read_dishtags(db: SessionLocal = Depends(get_db)):
#     dishtags = db.query(DishTags).all()
#     return dishtags
#
#
# @app.post("/dishtags")
# async def add_dishtag(
#         dish_id: int = Body(),
#         tag_id: int = Body(),
#         db: SessionLocal = Depends(get_db)
# ):
#     dishtag_id = max([row[0] for row in db.query(DishTags.id).all()] + [-1]) + 1
#     dishtag = Dishes(
#         id=dishtag_id,
#         dish_id=dish_id,
#         tag_id=tag_id
#     )
#     db.add(dishtag)
#     db.commit()
#     return dishtag_id
#
#
# @app.get("/dishtags/{dishtag_id}")
# async def read_dishtag_by_id(dishtag_id: int, db: SessionLocal = Depends(get_db)):
#     dishtag = db.query(DishTags).filter(DishTags.id == dishtag_id).first()
#     return dishtag
#
#
# @app.delete("/dishtags/{dishtags_id}")
# async def delete_dishtag(dishtag_id: int, db: SessionLocal = Depends(get_db)):
#     dishtag = db.query(DishTags).filter(DishTags.id == dishtag_id).first()
#     if not dishtag:
#         raise HTTPException(status_code=404, detail="DishTag not found")
#     db.delete(dishtag)
#     db.commit()


@app.get("/get_tags_map")
async def get_tags_map():
    return {
        0: "vege",
        1: "glutenFree",
        2: "sugarFree",
        3: "shouldBeWarm",
        4: "spicy"
    }


# @app.post("/add_tags_to_dish")
# async def add_tags_to_dish(dish_id: int, list_of_tag_id: list[int]):
#     for tag_id in list_of_tag_id:
#         add_dishtag(dish_id, tag_id)


