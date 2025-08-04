from uuid import UUID

from app.entities.base import BaseModel
from app.entities.review import Review


class User(BaseModel):
    id: UUID | None = None
    name: str
    email: str
    reviews: list[Review]
