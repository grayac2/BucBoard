from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Campus(Base):
    __tablename__ = 'Campus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(255))
    state = Column(String(255))
    name = Column(String(255))

