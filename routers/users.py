from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from starlette.status import HTTP_204_NO_CONTENT

from services.response import HTTP_404_NOT_FOUND
from models.users import Users, User_Pydantic, UserIn


tags=["users"]

router = APIRouter()


@router.post("/users", tags=tags, response_model=User_Pydantic)
async def create(form_data: UserIn):
    user = await Users.create(**form_data.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user)
