import datetime

import pydantic

from src.models.schemas.base import BaseSchemaModel


class AuthorInCreate(BaseSchemaModel):
    name: str


class AuthorInUpdate(BaseSchemaModel):
    name: str | None


class AuthorInResponse(BaseSchemaModel):
    id: int
    name: str
