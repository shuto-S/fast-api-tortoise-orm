from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from models.users import Users


tags = ["token"]
router = APIRouter()


class LoginIn(BaseModel):
    email: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", tags=tags, response_model=LoginOut)
async def login_with_password(form_data: LoginIn):
    user = await Users.login(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return LoginOut(access_token=user.get_access_token())
