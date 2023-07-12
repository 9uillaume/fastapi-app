import datetime

import pydantic

from src.models.schemas.base import BaseSchemaModel


class BookInCreate(BaseSchemaModel):
    name: str
    author_id: int


class BookInUpdate(BaseSchemaModel):
    name: str | None
    author_id: int


class BookInResponse(BaseSchemaModel):
    id: int
    name: str
    author_id: int
