from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

from services.auth import get_password_hash


class Users(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, required=True, unique=True)
    hashed_password = fields.CharField(max_length=200, required=True)
    access_token = fields.CharField(max_length=255, null=True, unique=True)
    username = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    @classmethod
    def create(cls, **kwargs):
        kwargs["hashed_password"] = get_password_hash(kwargs["password"])
        return super().create(**kwargs)


User_Pydantic = pydantic_model_creator(Users, name="User", exclude=[
    "hashed_password",
    "access_token",
    "deleted_at"
])


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str
