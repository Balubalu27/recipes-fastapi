from fastapi import FastAPI
from fastapi_pagination import add_pagination

from recipes.api import router
from recipes.database import engine
from recipes.tables import Base

tags_metadata = [
    {
        'name': 'Admin',
        'description': 'Блокировка/разблокировка пользователей и рецептов'
    },
    {
        'name': 'Auth',
        'description': 'Авторизация и регистрация'
    },
    {
        'name': 'Recipes',
        'description': 'Работа с рецептами'
    },
    {
        'name': 'Users',
        'description': 'Работа с пользователями'
    }
]

app = FastAPI(
    title='Сервис пользовательских рецептов',
    description='API для работы с рецептами/пользователями',
    version='1.0.0',
    openapi_tags=tags_metadata
)


@app.get('/')
async def root():
    return {'Главная страница': 'Для работы с API перейдите на 0.0.0.0:8001/docs'}

app.include_router(router)

add_pagination(app)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
