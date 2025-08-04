from uuid import UUID

from app.entities.base import BaseModel


class Review(BaseModel):
    id: UUID | None = None
    book_id: UUID
    user_id: UUID
    rating: float
    text: str
