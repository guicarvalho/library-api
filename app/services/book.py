from datetime import datetime
from http import HTTPStatus
import operator
import uuid

from fastapi import HTTPException


from app.database import BOOKS
from app.entities.book import Book
from app.entities.review import Review
from app.utils.pagination import Metadata, Page


async def create_book(title: str, genre: str) -> Book:
    book = Book(
        id=uuid.uuid4(),
        title=title,
        genre=genre,
        reviews=[],
        average_rating=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    BOOKS.append(book)
    return book


async def list_all_books(title: str | None, genre: str | None) -> Page[Book]:
    filtered_books = [
        book
        for book in BOOKS
        if (title is None or book.title == title)
        and (genre is None or book.genre == genre)
    ]
    filtered_books_total = len(filtered_books)
    return Page(
        data=filtered_books,
        meta=Metadata(
            total=filtered_books_total, page=1, size=filtered_books_total
        ),
    )


async def get_book_reviews(
    book_id: uuid.UUID, rating: float | None = None
) -> Page[Review]:
    books = [book for book in BOOKS if book.id == book_id]
    if not books:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Book not found"
        )
    book = books[0]
    reviews = [
        review
        for review in book.reviews
        if rating is None or review.rating >= rating
    ]
    sorted_reviews = sorted(
        reviews, key=operator.attrgetter("rating"), reverse=True
    )

    sorted_reviews_total = len(sorted_reviews)
    return Page(
        data=sorted_reviews,
        meta=Metadata(
            total=sorted_reviews_total, page=1, size=sorted_reviews_total
        ),
    )
