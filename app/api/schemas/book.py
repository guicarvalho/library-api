from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.api.schemas.review import ReviewOut


class BaseBook(BaseModel):
    title: str
    genre: str


class BookCreateIn(BaseBook):
    pass


class BookOut(BaseBook):
    id: UUID
    reviews: list[ReviewOut]
    average_rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
