import uuid

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from .base import BaseModel
from app.services import auth


class User(BaseModel):
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=200, null=True)
    refresh_token = fields.UUIDField(null=True)
    username = fields.CharField(max_length=100, required=True)

    @classmethod
    async def get_active_user(cls, user_id: int = None, email: str = None):
        if user_id is not None:
            return await cls.get_or_none(id=user_id, deleted_at=None)
        if email is not None:
            return await cls.get_or_none(email=email, deleted_at=None)
        return None

    @classmethod
    def create(cls, **kwargs):
        kwargs["hashed_password"] = auth.get_password_hash(kwargs["password"])
        kwargs["refresh_token"] = uuid.uuid4().hex
        return super().create(**kwargs)

    def get_access_token(self):
        return auth.create_access_token(data={
            "sub": self.email,
            "username": self.username
        })


User_Pydantic = pydantic_model_creator(User, name="User", include=(
    "email",
    "username",
))

UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", include=(
    "username",
), exclude_readonly=True)
