import bcrypt
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship, declarative_base
from .shered import Base


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


# utils

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

def get_user_by_username(username, db):
    return db.query(Users).filter_by(login=username).first()
