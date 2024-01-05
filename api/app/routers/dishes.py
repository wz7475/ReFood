from fastapi import APIRouter, Depends, HTTPException, Body
from ..utils.sessions import cookie, verifier, SessionData
from ..utils.sqlalchemy import SessionLocal, get_db
from ..models.offers import Dishes
from ..models.users import Users, get_user_by_username


router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
    dependencies=[Depends(cookie)],
    responses={404: {"description": "Not found"}},
)


@router.get("/mine")
async def read_offers(db: SessionLocal = Depends(get_db), session_data: SessionData = Depends(verifier)):
    user_id = get_user_by_username(session_data.username)
    dishes = db.query(Dishes).filter_by(author_id=int(user_id)).all()
    return dishes


@router.get("/{dish_id}", dependencies=[Depends(cookie)])
async def read_dishes_by_id(dish_id: int, db: SessionLocal = Depends(get_db),
                            session_data: SessionData = Depends(verifier)):
    user_id = get_user_by_username(session_data.username)
    dish = db.query(Dishes).filter(Dishes.id == dish_id).filter_by(author_id=int(user_id)).all()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@router.delete("/{dish_id}")
async def delete_dish(dish_id: int, db: SessionLocal = Depends(get_db)):
    dish = db.query(Dishes).filter(Dishes.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()


@router.post("/dishes", dependencies=[Depends(cookie)])
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
