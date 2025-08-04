from http import HTTPStatus
import uuid

from fastapi import APIRouter

from app.api.schemas.book import BookCreateIn, BookOut
from app.api.schemas.review import ReviewOut
from app.api.schemas.shared import Page
from app.services.book import create_book, get_book_reviews, list_all_books

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    response_model=BookOut,
    status_code=HTTPStatus.CREATED,
    summary="Create book",
)
async def create(data: BookCreateIn):
    return await create_book(title=data.title, genre=data.genre)


@router.get(
    "/",
    response_model=Page[BookOut],
    summary="List books",
)
async def list_all(title: str | None = None, genre: str | None = None):
    return await list_all_books(title=title, genre=genre)


@router.get(
    "/{id}/reviews",
    response_model=Page[ReviewOut],
    summary="Book reviews",
)
async def get_reviews(id: uuid.UUID, rating: float | None = None):
    return await get_book_reviews(book_id=id, rating=rating)
