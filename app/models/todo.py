from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from .base import BaseModel


class Todo(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="users")
    name = fields.CharField(max_length=100)
    memo = fields.TextField(null=True)
    completed = fields.BooleanField(null=True, default=False)
    completed_at = fields.DatetimeField(null=True)


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo", exclude=("deleted_at",))
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", include=(
    "name",
    "memo",
), exclude_readonly=True)
