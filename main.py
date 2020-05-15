from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from configs.db import DB_CONFIG
from routers import routers


app = FastAPI()

# routersを登録
for router in routers:
    app.include_router(router)

# DB
register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=True,
    add_exception_handlers=True,
)
