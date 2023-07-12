import typing

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.author import Author
from src.models.schemas.author import AuthorInCreate, AuthorInUpdate
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist


class AuthorCRUDRepository(BaseCRUDRepository):
    async def create_author(self, author_create: AuthorInCreate) -> Author:
        new_author = Author(
            name=author_create.name,
        )

        self.async_session.add(instance=new_author)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_author)

        return new_author

    async def read_authors(self) -> typing.Sequence[Author]:
        stmt = sqlalchemy.select(Author)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_author_by_id(self, id: int) -> Author:
        stmt = sqlalchemy.select(Author).where(Author.id == id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Author with id `{id}` does not exist!")

        return query.scalar()  # type: ignore

    async def read_author_by_name(self, name: str) -> Author:
        stmt = sqlalchemy.select(Author).where(Author.username == name)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist("Author with name `{name}` does not exist!")

        return query.scalar()  # type: ignore

    async def update_author_by_id(
        self, id: int, author_update: AuthorInUpdate
    ) -> Author:
        new_author_data = author_update.dict()

        select_stmt = sqlalchemy.select(Author).where(Author.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_author = query.scalar()

        if not update_author:
            raise EntityDoesNotExist(f"Author with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Author).where(Author.id == update_author.id).values(updated_at=sqlalchemy_functions.now())  # type: ignore

        if new_author_data["name"]:
            update_stmt = update_stmt.values(name=new_author_data["name"])

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_author)

        return update_author  # type: ignore

    async def delete_author_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(Author).where(Author.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_author = query.scalar()

        if not delete_author:
            raise EntityDoesNotExist(f"Author with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=Author).where(Author.id == delete_author.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Author with id '{id}' is successfully deleted!"
