from uuid import UUID

from app.entities.base import BaseModel
from app.entities.review import Review


class Book(BaseModel):
    id: UUID | None = None
    title: str
    genre: str
    reviews: list[Review]
    average_rating: float
