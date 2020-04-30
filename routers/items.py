from fastapi import APIRouter, Depends, HTTPException
from typing import List
from databases import Database
from starlette.status import HTTP_204_NO_CONTENT

from utils import get_db_connection
from schemas import items
from models.item import ItemModel


router = APIRouter()

@router.get("/items", tags=["items"], response_model=List[ItemModel])
async def list_item(database: Database = Depends(get_db_connection)):
    query = items.select()
    return await database.fetch_all(query)

@router.post("/items", tags=["items"], response_model=ItemModel)
async def create_item(data: ItemModel, database: Database = Depends(get_db_connection)):
    query = items.insert()
    await database.execute(query, data.dict())
    return {**data.dict()}

@router.patch("/items/{item_id}", tags=["items"], response_model=ItemModel)
async def update_item(item_id: int, data: ItemModel, database: Database = Depends(get_db_connection)):
    query = items.update().where(items.columns.id==item_id)
    ret = await database.execute(query, data.dict())
    if not ret:
        raise HTTPException(status_code=404, detail="Not Found")
    return {**data.dict()}

@router.delete("/items/{item_id}", tags=["items"], status_code=HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, database: Database = Depends(get_db_connection)):
    query = items.delete().where(items.columns.id==item_id)
    ret = await database.execute(query)
    if not ret:
        raise HTTPException(status_code=404, detail="Not Found")
