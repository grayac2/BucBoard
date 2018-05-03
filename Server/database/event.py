from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Events(Base):
    __tablename__ = 'Events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    host = Column(String(255))
    image = Column(BLOB)
    start = Column(DateTime)
    end = Column(DateTime)
    room_num = Column(Integer)

