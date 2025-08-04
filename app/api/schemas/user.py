from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.api.schemas.review import ReviewOut


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class UserCreateIn(BaseUser):
    pass


class UserUpdateIn(BaseUser):
    name: str | None = None
    email: str | None = None


class UserOut(BaseUser):
    id: UUID
    name: str
    email: EmailStr
    reviews: list[ReviewOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
