from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from .base import BaseModel
from services import auth


class Users(BaseModel):
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=200, null=True)
    access_token = fields.CharField(max_length=255, null=True, unique=True)
    username = fields.CharField(max_length=100, required=True)

    @classmethod
    async def get_active_user(cls, id: int = None, email: str = None):
        if id is not None:
            return await cls.get_or_none(id=id, deleted_at=None)
        if email is not None:
            return await cls.get_or_none(email=email, deleted_at=None)
        return None

    @classmethod
    def create(cls, **kwargs):
        kwargs["hashed_password"] = auth.get_password_hash(kwargs["password"])
        return super().create(**kwargs)

    def get_access_token(self):
        if self.access_token:
            return self.access_token
        access_token = auth.create_access_token(data={
            "sub": self.email,
            "username": self.username
        })
        self.access_token = access_token
        self.save()
        return access_token


User_Pydantic = pydantic_model_creator(Users, name="User", exclude=[
    "hashed_password",
    "access_token",
    "deleted_at",
])

UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", include=[
    "username",
], exclude_readonly=True)
