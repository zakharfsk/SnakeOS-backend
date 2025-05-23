from tortoise import fields
from .base import BaseModel


class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True, index=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.email


class Session(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="sessions")
    token = fields.CharField(max_length=500)
    is_active = fields.BooleanField(default=True)
    expires_at = fields.DatetimeField()

    class Meta:
        table = "sessions"

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
