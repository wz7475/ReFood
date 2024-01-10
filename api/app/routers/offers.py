from fastapi import APIRouter, Depends, HTTPException, Body, BackgroundTasks
from ..utils.sessions import cookie, verifier, SessionData
from ..utils.sqlalchemy import SessionLocal, get_db
from ..utils.es_tools import get_by_fulltext, get_by_fulltext_distance
from ..models.offers import (read_all_open_offers, read_open_offers_by_offer_id, Offers, Dishes, convert_offers,
                             Outbox, read_bought_offers,
                             read_sold_offers, add_users, add_offer_db, read_all_offers, OfferState, change_offer_state)
from ..models.users import Users, get_user_name, get_user_surname, get_user_by_username
from ..models.dishes import TagsValues, add_dish
from ..utils.cfg import DELETE_OFFER_QUEUE, OFFER_INDEX
from ..utils.backgroundtasks import send_messages_from_outbox
from ..utils.connectors import connections
from ..utils.logger import get_logger
from typing import List
import json

router = APIRouter(
    prefix="/offers",
    tags=["offers"],
    dependencies=[Depends(cookie)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_offers(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    offers_db = read_all_open_offers(db)
    offers = convert_offers(offers_db)
    return offers


@router.post("/filter")
async def read_offers(
        pattern: str = Body(),
        tags: List[int] = Body(),
        distance: float = Body(),
        lat: float = Body(),
        lon: float = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)):
    fields = ["description", "dish_name"]
    if distance > 0:
        result = get_by_fulltext_distance(connections["es"], OFFER_INDEX, fields, pattern, tags, distance, lat, lon)
    else:
        result = get_by_fulltext(connections["es"], OFFER_INDEX, fields, pattern, tags)
    get_logger().info(result)
    # return result
    hits = result["hits"]["hits"]
    offers = []
    for hit in hits:
        get_logger().info(f"hit id {hit['_id']}")
        cur_offers = read_open_offers_by_offer_id(db, hit["_id"])
        if cur_offers:
            offers.append(convert_offers(cur_offers)[0])
    return offers


@router.get("/mine")
async def read_offers(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    user = get_user_by_username(session_data.username, db)

    sell_query_result = read_sold_offers(user.id, db)
    sell_offers = convert_offers(sell_query_result)

    buy_query_result = read_bought_offers(user.id, db)
    buy_offers = convert_offers(buy_query_result)

    offers = []
    for offer in sell_offers:
        offers.append(add_users(offer, selling=True, db=db))
    for offer in buy_offers:
        offers.append(add_users(offer, selling=False, db=db))
    return offers


@router.post("/")
async def add_offer(
        background_tasks: BackgroundTasks,
        latitude: float = Body(),
        longitude: float = Body(),
        dish_name: str = Body(),
        description: str = Body(),
        price: int = Body(),  # price in grosze
        how_many_days_before_expiration: float = Body(),
        tags: List[int] = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user = get_user_by_username(session_data.username, db)

    enum_tags = []
    for tag_val in tags:
        enum_tags.append(TagsValues(tag_val))

    dish_id = add_dish(db, dish_name, description, how_many_days_before_expiration, user.id, enum_tags)
    offer_id = add_offer_db(db, dish_id, latitude, longitude, price, user.id)

    background_tasks.add_task(send_messages_from_outbox, connections["add-channel"], connections["logger"])
    return offer_id


@router.post("/dish")
async def add_offer(
        dish_id: int = Body(),
        latitude: float = Body(),
        longitude: float = Body(),
        price: int = Body(),  # price in grosze
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user = get_user_by_username(session_data.username, db)

    # valid if dish exists
    if not db.query(Dishes).filter(Dishes.id == dish_id).first():
        raise HTTPException(status_code=404, detail="Dish not found")

    offer_id = add_offer_db(db, dish_id, latitude, longitude, price, user.id)
    return offer_id


@router.get("/{offer_id}")
async def read_offer_by_id(offer_id: int, db: SessionLocal = Depends(get_db),
                           session_data: SessionData = Depends(verifier)):
    query_result = read_all_offers(db)
    offers = convert_offers(query_result, offer_id)
    rdy_offers = []
    for offer in offers:
        buyer_id = offer["buyer_id"]
        offer["buyer_name"] = get_user_name(buyer_id, db)
        offer["buyer_surname"] = get_user_surname(buyer_id, db)
        rdy_offers.append(offer)
    if not rdy_offers:
        raise HTTPException(status_code=404, detail="Offer not found")
    return rdy_offers


@router.delete("/{offer_id}", dependencies=[Depends(cookie)])
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


@router.get("/complete/{offer_id}", dependencies=[Depends(cookie)])
async def complete_offer(
        offer_id: int,
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user = get_user_by_username(session_data.username, db)
    if not change_offer_state(db, offer_id, user.id, OfferState.COMPLETED):
        HTTPException(status_code=404, detail="Offer not found")
    return "ok"


@router.post("/reserve", dependencies=[Depends(cookie)])
async def reserve_offer(
        offer_id: int = Body(),
        db: SessionLocal = Depends(get_db),
        session_data: SessionData = Depends(verifier)
):
    user = get_user_by_username(session_data.username, db)
    if not change_offer_state(db, offer_id, user.id, OfferState.RESERVED):
        HTTPException(status_code=404, detail="Offer not found")
    return "ok"