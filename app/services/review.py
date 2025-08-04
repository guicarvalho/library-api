from datetime import datetime
from http import HTTPStatus
import uuid

from fastapi import HTTPException


from app.database import BOOKS
from app.entities.book import Book
from app.entities.review import Review
from app.services.user import get_user


async def _get_book(id: uuid.UUID) -> Book:
    filtered_books = [book for book in BOOKS if book.id == id]
    if not filtered_books:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found"
        )
    return filtered_books[0]


async def _calculate_average_rating(reviews: list[Review]) -> float:
    if not reviews:
        return 0
    return sum(review.rating for review in reviews) / len(reviews)


async def create_review(
    user_id: uuid.UUID, book_id: uuid.UUID, text: str, rating: float
) -> Review:
    user = await get_user(id=user_id)
    book = await _get_book(id=book_id)
    book_reviews = book.reviews

    # create new review
    new_review = Review(
        id=uuid.uuid4(),
        user_id=user_id,
        book_id=book_id,
        text=text,
        rating=rating,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # update review list in user and book
    book_reviews.append(new_review)
    user.reviews.append(new_review)

    # update book average rating
    book.average_rating = await _calculate_average_rating(book.reviews)

    return new_review
