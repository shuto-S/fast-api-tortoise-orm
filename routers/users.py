from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.status import HTTP_204_NO_CONTENT

from services.auth import get_current_user
from models.user import User, User_Pydantic, UserIn_Pydantic


tags = ["users"]
router = APIRouter()


class UserIn(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register", tags=tags, response_model=User_Pydantic)
async def register_user(form_data: UserIn):
    return await User.create(**form_data.dict(exclude_unset=True))


@router.get("/me", tags=tags, response_model=User_Pydantic)
async def get_user_data(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", tags=tags, response_model=User_Pydantic)
async def update_user(form_data: UserIn_Pydantic, user: User = Depends(get_current_user)):
    await user.update_from_dict(form_data.dict(exclude_unset=True)).save()
    return user


@router.delete("/me", tags=tags, status_code=HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_current_user)):
    await user.soft_delete()
