from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.auth import get_current_user
from models.users import Users, User_Pydantic


tags = ["users"]
router = APIRouter()


class UserIn(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register", tags=tags, response_model=User_Pydantic)
async def register_user(form_data: UserIn):
    user = await Users.create(**form_data.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user)


@router.get("/me", tags=tags, response_model=User_Pydantic)
async def get_user_data(user: Users = Depends(get_current_user)):
    return await User_Pydantic.from_tortoise_orm(user)
