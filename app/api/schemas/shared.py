from pydantic import BaseModel


class Metadata(BaseModel):
    total: int
    page: int
    size: int


class Page[T](BaseModel):
    data: list[T]
    meta: Metadata
