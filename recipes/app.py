from fastapi import FastAPI
from fastapi_pagination import add_pagination

from recipes.api import router
from recipes.database import engine
from recipes.tables import Base

app = FastAPI()
app.include_router(router)

add_pagination(app)

# @app.on_event("startup")
# async def startup():
#     # create db tables
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
