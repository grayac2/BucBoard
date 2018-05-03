from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OfficeHours(Base):
    __tablename__ = 'Office_Hours'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime)
    end = Column(DateTime)
    professor = Column(Integer)
    room_num = Column(Integer)
