from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from starlette.status import HTTP_204_NO_CONTENT

from models import Item_Pydantic, ItemIn_Pydantic, Items


router = APIRouter()

@router.get("/items", tags=["items"], response_model=List[Item_Pydantic])
async def list_items():
    return await Item_Pydantic.from_queryset(Items.all())

@router.post("/items", tags=["items"], response_model=Item_Pydantic)
async def create_item(item: ItemIn_Pydantic):
    item_obj = await Items.create(**item.dict(exclude_unset=True))
    return await Item_Pydantic.from_tortoise_orm(item_obj)

@router.patch("/items/{item_id}", tags=["items"], response_model=Item_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_item(item_id: int, item: ItemIn_Pydantic):
    await Items.filter(id=item_id).update(**item.dict(exclude_unset=True))
    return await Item_Pydantic.from_queryset_single(Items.get(id=item_id))

@router.delete("/items/{item_id}", tags=["items"], status_code=HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    deleted_count = await Items.filter(id=item_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Not found")
