from fastapi import Depends
from sqlalchemy.orm import Session
from recipes import tables
from recipes.database import get_session


class RecipesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> list[tables.Recipe]:
        recipes = (
            self.session
            .query(tables.Recipe)
            .filter(tables.Recipe.is_active == True)
            .all()
        )
        return recipes
