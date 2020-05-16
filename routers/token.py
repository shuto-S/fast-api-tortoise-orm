from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services.auth import login_with_password


tags = ["token"]
router = APIRouter()


class LoginIn(BaseModel):
    email: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", tags=tags, response_model=LoginOut)
async def get_token_with_password(form_data: LoginIn):
    user = await login_with_password(form_data.email, form_data.password)
    return LoginOut(access_token=user.get_access_token())
