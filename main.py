from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from configs.db import db_config
from routers import routers


app = FastAPI()

# routersを登録
for router in routers:
    app.include_router(router)

# DB
register_tortoise(
    app,
    config=db_config,
    generate_schemas=True,
    add_exception_handlers=True,
)
