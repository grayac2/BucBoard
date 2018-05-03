from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Building(Base):
    __tablename__ = 'Building'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    campus = Column(Integer)

