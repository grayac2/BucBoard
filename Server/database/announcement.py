from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Announcements(Base):
    __tablename__ = 'Announcements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    info = Column(Text)
    image = Column(BLOB)
    professor = Column(Integer)
    room_num = Column(Integer)

