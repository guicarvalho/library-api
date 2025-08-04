from http import HTTPStatus

from fastapi import APIRouter

from app.api.schemas.review import ReviewCreateIn, ReviewOut
from app.services.review import create_review

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post(
    "/",
    response_model=ReviewOut,
    status_code=HTTPStatus.CREATED,
    summary="Create review",
)
async def create(data: ReviewCreateIn):
    return await create_review(
        user_id=data.user_id,
        book_id=data.book_id,
        text=data.text,
        rating=data.rating,
    )
