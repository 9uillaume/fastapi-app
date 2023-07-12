import datetime

import sqlalchemy
from sqlalchemy.orm import (
    Mapped as SQLAlchemyMapped,
    mapped_column as sqlalchemy_mapped_column,
)
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.table import Base


class Book(Base):  # type: ignore
    __tablename__ = "book"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True, autoincrement="auto"
    )
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    author_id = sqlalchemy_mapped_column(ForeignKey("author.id"), unique=True)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}
