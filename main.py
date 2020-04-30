from fastapi import FastAPI
from db import database
from starlette.requests import Request
from routers import items

app = FastAPI()

@app.on_event("startup")
async def startup():
    # DBコネクション開始
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # DBコネクション切断
    await database.disconnect()

# routersを登録
app.include_router(items.router)

# ミドルウェアでDBコネクション埋め込んでおく（routerで取得できるように）
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.connection = database
    response = await call_next(request)
    return response
