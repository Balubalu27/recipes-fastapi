from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Numeric, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

