from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Room(Base):
    __tablename__ = 'Room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer)
    room_num = Column(Integer)
    building = Column(Integer)

