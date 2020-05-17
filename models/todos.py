from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from .base import BaseModel


class Todos(BaseModel):
    name = fields.CharField(max_length=100)
    memo = fields.TextField(null=True)
    complited = fields.BooleanField(null=True, default=False)
    complited_at = fields.DatetimeField(null=True)

    user = fields.ForeignKeyField("models.Users", related_name="users")


Todo_Pydantic = pydantic_model_creator(Todos, name="Todo", exclude=["deleted_at"])
TodoIn_Pydantic = pydantic_model_creator(Todos, name="TodoIn", include=[
    "name",
    "memo",
], exclude_readonly=True)
