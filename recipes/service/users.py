from fastapi import Depends
from sqlalchemy.orm import Session
from recipes import tables
from recipes.database import get_session


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> list[tables.User]:
        users = (
            self.session
            .query(tables.User)
            .filter(tables.User.is_active == True)
            .all()
        )
        return users
