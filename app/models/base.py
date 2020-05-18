from datetime import datetime

from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)
    deleted_at = fields.DatetimeField(null=True)

    async def soft_delete(self):
        self.deleted_at = datetime.now()
        await self.save(update_fields=["deleted_at"])
