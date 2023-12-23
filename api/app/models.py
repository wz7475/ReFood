import enum
from sqlalchemy import Column, Integer, String, Enum, Sequence, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, Sequence("users_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    login = Column(String)
    phone_nr = Column(String(9))

    offers = relationship("Offers", back_populates="seller")


class Dishes(Base):
    __tablename__ = "Dishes"

    id = Column(Integer, Sequence("dishes_id_seq"), primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    how_many_days_before_expiration = Column(Float)

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
    creation_date = Column(DateTime)

    seller = relationship("Users", back_populates="offers")
    dishes = relationship("Dishes", back_populates="offers")

class TagsValues(enum.Enum):
    VEGETARIAN = 0
    GLUTEN_FREE = 1
    SUGAR_FREE = 2
    SHOULD_BE_EATEN_WARM = 3
    SPICY = 4

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
