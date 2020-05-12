from fastapi import APIRouter, HTTPException, status

from models.users import Users, LoginIn, LoginOut
from services.auth import authenticate_user, create_access_token

tags=["token"]

router = APIRouter()

@router.post("/token", tags=tags, response_model=LoginOut)
async def login_for_access_token(form_data: LoginIn):
    user = await authenticate_user(Users, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.access_token:
        access_token = create_access_token(data={"sub": user.username})
        user.access_token = access_token
        await user.save()
    return {"access_token": user.access_token, "token_type": "bearer"}
