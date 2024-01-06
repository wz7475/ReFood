
from contextlib import asynccontextmanager

from fastapi import FastAPI, Body, HTTPException, Depends, Response

from .utils.logger import get_logger
from .utils.cfg import ADD_OFFER_QUEUE, DELETE_OFFER_QUEUE, OFFER_INDEX
from .utils.connectors import get_rabbitmq_connection, get_es_connection, connections
from .utils.sessions import SessionData, backend, cookie, verifier
from .utils.sqlalchemy import engine, SessionLocal, get_db
from .models.shered import Base
from .models.users import Users
from .models.dishes import get_tags_map_low
from uuid import UUID, uuid4
from .routers import offers, dishes
from .utils.es_tools import get_all_data # TODO delete




@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger()
    Base.metadata.create_all(bind=engine)
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


app.include_router(offers.router)
app.include_router(dishes.router)



@app.get("/")
async def root():
    return get_all_data(connections["es"], OFFER_INDEX)
    # return {"message": "Hello Refood multiple files"}


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


@app.get("/get_tags_map")
async def get_tags_map():
    return get_tags_map_low()
