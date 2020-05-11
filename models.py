from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Items(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()


Item_Pydantic = pydantic_model_creator(Items, name="Item")
ItemIn_Pydantic = pydantic_model_creator(Items, name="ItemIn", exclude_readonly=True)
