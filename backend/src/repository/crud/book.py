import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.book import Book
from src.models.schemas.book import BookInCreate, BookInUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist


class BookCRUDRepository(BaseCRUDRepository):
    async def create_book(self, book_create: BookInCreate) -> Book:
        new_book = Book(name=book_create.name, author_id=book_create.author_id)

        self.async_session.add(instance=new_book)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_book)

        return new_book

    async def read_books(self) -> typing.Sequence[Book]:
        stmt = sqlalchemy.select(Book)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_book_by_id(self, id: int) -> Book:
        stmt = sqlalchemy.select(Book).where(Book.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Book with id `{id}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_book_by_author_id(self, author_id: int) -> Book:
        stmt = sqlalchemy.select(Book).where(Book.author_id == author_id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "Book with author id `{author_id}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def read_book_by_name(self, name: str) -> Book:
        stmt = sqlalchemy.select(Book).where(Book.username == name)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Book with name `{name}` does not exist!")

        return query.scalar()  # type: ignore

    async def update_book_by_id(self, id: int, book_update: BookInUpdate) -> Book:
        new_book_data = book_update.dict()

        select_stmt = sqlalchemy.select(Book).where(Book.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_book = query.scalar()

        if not update_book:
            raise EntityDoesNotExist(f"Book with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Book).where(Book.id == update_book.id).values(updated_at=sqlalchemy_functions.now())  # type: ignore

        if new_book_data["name"]:
            update_stmt = update_stmt.values(name=new_book_data["name"])

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_book)

        return update_book  # type: ignore

    async def delete_book_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(Book).where(Book.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_book = query.scalar()

        if not delete_book:
            raise EntityDoesNotExist(f"Book with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=Book).where(Book.id == delete_book.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Book with id '{id}' is successfully deleted!"
