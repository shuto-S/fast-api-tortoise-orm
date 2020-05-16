from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from configs.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models.users import Users
from services.response import HTTP_401_AUTHENTICATE_EXCEPTION


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(*, data: dict) -> str:
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt.decode()


async def login_with_password(email: str, password: str) -> Users:
    user = await Users.get_active_user(email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTP_401_AUTHENTICATE_EXCEPTION
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await Users.get_active_user(email=payload.get("sub"))
    except jwt.PyJWTError:
        raise HTTP_401_AUTHENTICATE_EXCEPTION
    if not user:
        raise HTTP_401_AUTHENTICATE_EXCEPTION
    return user
