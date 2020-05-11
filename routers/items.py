from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from starlette.status import HTTP_204_NO_CONTENT

from utiles.response import HTTP_404_NOT_FOUND
from models.items import Item_Pydantic, ItemIn_Pydantic, Items


end_point = "items"
tags=["items"]
model = Items
model_pydanic = Item_Pydantic
model_in_pydanic = ItemIn_Pydantic

router = APIRouter()

@router.get("/{end_point}", tags=tags, response_model=List[model_pydanic])
async def get_list():
    return await model_pydanic.from_queryset(model.all())

@router.post("/{end_point}", tags=tags, response_model=model_pydanic)
async def create(data: model_in_pydanic):
    obj = await model.create(**data.dict(exclude_unset=True))
    return await model_pydanic.from_tortoise_orm(obj)

@router.patch("/{end_point}/{id}", tags=tags, response_model=model_pydanic, responses=HTTP_404_NOT_FOUND)
async def update(id: int, data: model_in_pydanic):
    await model.filter(id=id).update(**data.dict(exclude_unset=True))
    return await model_pydanic.from_queryset_single(model.get(id=id))

@router.delete("/{end_point}/{id}", tags=tags, status_code=HTTP_204_NO_CONTENT)
async def delete(id: int):
    deleted_count = await model.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Not found")
