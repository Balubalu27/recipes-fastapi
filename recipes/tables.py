from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Numeric, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    recipes = relationship("Recipe", back_populates="author")
    # favorites = Column() - ManyToMany на рецепты
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(DateTime, onupdate=datetime.now())


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", back_populates="recipes")
    dish_type = Column(String(20))
    description = Column(String, nullable=True)
    cooking_steps = Column(String)
    photo_link = Column(String)
    # likes = Column()
    # hashtags = Column()
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(DateTime, onupdate=datetime.now())


