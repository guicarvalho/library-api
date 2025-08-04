import uuid
from http import HTTPStatus

from fastapi import APIRouter

from app.api.schemas.shared import Page
from app.api.schemas.user import UserCreateIn, UserOut, UserUpdateIn
from app.services.user import create_user, get_user, list_all_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=HTTPStatus.CREATED,
    summary="Create user",
)
async def create(data: UserCreateIn):
    return await create_user(name=data.name, email=data.email)


@router.get(
    "/",
    response_model=Page[UserOut],
    summary="List users",
)
async def list_all():
    return await list_all_users()


@router.get(
    "/{id}",
    response_model=UserOut,
    summary="Get user by id",
)
async def get_by_id(id: uuid.UUID):
    return await get_user(id=id)


@router.patch(
    "/{id}",
    response_model=UserOut,
    summary="Update user",
)
async def update(id: uuid.UUID, data: UserUpdateIn):
    return await update_user(id=id, name=data.name, email=data.email)
