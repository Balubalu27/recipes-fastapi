from fastapi import FastAPI
from recipes.api import router


app = FastAPI()
app.include_router(router)

