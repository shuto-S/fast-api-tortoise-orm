from fastapi import HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError


HTTP_404_NOT_FOUND = {404: {"model": HTTPNotFoundError}}


HTTP_401_AUTHENTICATE_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Authenticate",
    headers={"WWW-Authenticate": "Bearer"},
)
