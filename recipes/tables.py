from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin, relationship

Base = declarative_base()


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())


@declarative_mixin
class IsActiveMixin:
    is_active = Column(Boolean, default=True)


class User(TimestampMixin, IsActiveMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    recipes = relationship("Recipe", back_populates="author")


class Recipe(TimestampMixin, IsActiveMixin, Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", back_populates="recipes")
    dish_type = Column(String(20))
    description = Column(String, nullable=True)
    cooking_steps = Column(String)
    photo_link = Column(String)
    likes = Column(Integer, default=0)
