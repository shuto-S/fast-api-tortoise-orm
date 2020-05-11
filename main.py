from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from configs.db import db_config
from routers import items


app = FastAPI()

# routersを登録
app.include_router(items.router)

# DB
register_tortoise(
    app,
    config=db_config,
    generate_schemas=True,
    add_exception_handlers=True,
)
