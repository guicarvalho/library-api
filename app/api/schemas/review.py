from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseReview(BaseModel):
    book_id: UUID
    user_id: UUID
    rating: float
    text: str


class ReviewCreateIn(BaseReview):
    pass


class ReviewOut(BaseReview):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
