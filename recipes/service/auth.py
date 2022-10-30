from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from recipes import tables
from recipes.database import get_session
from recipes.models.auth import Token
from recipes.models.users import User, UserCreate
from recipes.service.exceptions import credentials_exception, is_blocked_exception, has_not_permissions_exception, \
    is_already_exists_exception
from recipes.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Получение текущего пользователя """
    return AuthService.validate_token(token)


def check_user_status(user: User):
    """ Проверка статуса пользователя активен/заблокирован """
    if not user.is_active:
        raise is_blocked_exception


def check_admin_permission(user: User):
    """ Проверка, является ли пользователь админом """
    if not user.is_superuser:
        raise has_not_permissions_exception


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """ Валидация пароля """
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """ Получить Хэш пароля """
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        """ Валидация токена """

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise credentials_exception
        user_data = payload.get('user')
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise credentials_exception
        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        """ Генерация токена """

        user_data = User.from_orm(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    async def register_new_user(self, user_data: UserCreate) -> Token:
        """ Регистрация пользователя """

        query = select(tables.User).where(tables.User.username == user_data.username)
        result = await self.session.execute(query)
        user = result.scalar()
        if user:
            raise is_already_exists_exception
        new_user = tables.User(
            username=user_data.username,
            password=self.hash_password(user_data.password)
        )
        self.session.add(new_user)
        await self.session.commit()
        return self.create_token(new_user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        """ Авторизация пользователя """

        query = select(tables.User).where(tables.User.username == username)
        result = await self.session.execute(query)
        user = result.scalars().first()

        if not user:
            raise credentials_exception

        if not self.verify_password(password, user.password):
            raise credentials_exception

        return self.create_token(user)
