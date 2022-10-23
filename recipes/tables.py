from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseMixin:
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, onupdate=func.now(), default=func.now())


class User(Base, BaseMixin):
    __tablename__ = 'users'

    username = Column(String(30), unique=True)
    password = Column(String)
    recipes = relationship("Recipe", back_populates="author")


class Recipe(Base, BaseMixin):
    __tablename__ = 'recipes'

    title = Column(String)
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", back_populates="recipes")
    dish_type = Column(String(20))
    description = Column(String, nullable=True)
    cooking_steps = Column(String)
    photo_link = Column(String)
    likes = Column(Integer, default=0)
