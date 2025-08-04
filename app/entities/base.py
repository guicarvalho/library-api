from datetime import datetime

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
