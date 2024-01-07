import enum

from sqlalchemy import Column, Integer, Enum, Sequence, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from .shered import Base


class TagsValues(enum.Enum):
    VEGETARIAN = 0
    GLUTEN_FREE = 1
    SUGAR_FREE = 2
    SHOULD_BE_WARM = 3
    SPICY = 4


class Dishes(Base):
    __tablename__ = "Dishes"

    id = Column(Integer, Sequence("dishes_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    how_many_days_before_expiration = Column(Float)
    author_id = Column(Integer, ForeignKey("Users.id"))
    tags = Column(MutableList.as_mutable(ARRAY(Enum(TagsValues))), nullable=True)

    author = relationship("Users", back_populates="dishes")
    offers = relationship("Offers", back_populates="dishes")


def add_dish(db, name, description, how_many_days_before_expiration, author_id, tags):
    dish_id = max([row[0] for row in db.query(Dishes.id).all()] + [-1]) + 1
    dish = Dishes(
        id=dish_id,
        name=name,
        description=description,
        how_many_days_before_expiration=how_many_days_before_expiration,
        author_id=author_id,
        tags=tags
    )
    db.add(dish)
    db.commit()
    return dish_id


def get_tags_map_low():
    tags = {}
    for tag in TagsValues:
        tags[tag.value] = tag.name.lower().replace("_", " ")
    return tags
