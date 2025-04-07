from tortoise import fields, models
from datetime import datetime


class BaseModel(models.Model):
    """
    Base model for all Tortoise ORM models.
    Includes common fields like id, created_at, and updated_at.
    """
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    async def save(self, *args, **kwargs):
        """
        Override save method to update the updated_at field
        """
        self.updated_at = datetime.now()
        await super().save(*args, **kwargs)

