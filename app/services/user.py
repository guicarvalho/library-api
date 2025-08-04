from datetime import datetime
from http import HTTPStatus
import uuid

from fastapi import HTTPException


from app.database import USERS
from app.entities.user import User
from app.utils.pagination import Metadata, Page


async def create_user(name: str, email: str) -> User:
    user = User(
        id=uuid.uuid4(),
        name=name,
        email=email,
        reviews=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    USERS.append(user)
    return user


async def list_all_users() -> Page[User]:
    return Page(
        data=USERS, meta=Metadata(total=len(USERS), page=1, size=len(USERS))
    )


async def get_user(id: uuid.UUID) -> User:
    filtered_users = [user for user in USERS if user.id == id]
    if not filtered_users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return filtered_users[0]


async def update_user(
    id: uuid.UUID, name: str | None, email: str | None
) -> User:
    user = await get_user(id=id)
    if name:
        user.name = name
    if email:
        user.email = email
    return user
