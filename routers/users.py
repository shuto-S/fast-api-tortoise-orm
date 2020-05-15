from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.response import HTTP_404_NOT_FOUND
from services.auth import get_current_user
from models.users import Users, User_Pydantic


tags=["users"]
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
async def get_user_data(user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await User_Pydantic.from_tortoise_orm(user)
