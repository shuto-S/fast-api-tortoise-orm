from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from services import auth


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
        kwargs["hashed_password"] = auth.get_password_hash(kwargs["password"])
        return super().create(**kwargs)

    @classmethod
    async def login(cls, email: str, password: str):
        user = await cls.get_or_none(email=email)
        if not user:
            return False
        if not auth.verify_password(password, user.hashed_password):
            return False
        return user

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
    "deleted_at"
])
