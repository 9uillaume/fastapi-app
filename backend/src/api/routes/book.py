import fastapi
import pydantic

from src.api.dependencies.repository import get_repository
from src.models.schemas.book import (
    BookInCreate,
    BookInResponse,
    BookInUpdate,
)
from src.repository.crud.book import BookCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)

router = fastapi.APIRouter(prefix="/books", tags=["books"])


@router.post(
    path="",
    name="bookss:create-books",
    response_model=BookInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_book(
    book_create: BookInCreate,
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> BookInResponse:
    db_book = await book_repo.create_book(book_create)

    return BookInResponse(id=db_book.id, name=db_book.name, author_id=db_book.author_id)


@router.get(
    path="",
    name="bookss:read-books",
    response_model=list[BookInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_books(
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> list[BookInResponse]:
    db_books = await book_repo.read_books()
    db_book_responses = [
        BookInResponse(id=book.id, name=book.name, author_id=book.author_id)
        for book in db_books
    ]
    return db_book_responses


@router.get(
    path="/{id}",
    name="bookss:read-book-by-id",
    response_model=BookInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_book(
    id: int,
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> BookInResponse:
    try:
        db_book = await book_repo.read_book_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return BookInResponse(id=db_book.id, name=db_book.name, author_id=db_book.author_id)


@router.get(
    path="/{author_id}",
    name="bookss:read-book-by-author-id",
    response_model=BookInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_book(
    author_id: int,
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> BookInResponse:
    try:
        db_book = await book_repo.read_book_by_author_id(author_id=author_id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return BookInResponse(id=db_book.id, name=db_book.name, author_id=db_book.author_id)


@router.patch(
    path="/{id}",
    name="bookss:update-book-by-id",
    response_model=BookInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_book(
    id: int,
    book_update: BookInUpdate,
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> BookInResponse:
    book_update = BookInUpdate(name=book_update.name, author_id=book_update.author_id)
    try:
        updated_db_book = await book_repo.update_book_by_id(
            id=id,
            book_update=book_update,
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return BookInResponse(
        id=updated_db_book.id,
        name=updated_db_book.name,
        author_id=updated_db_book.author_id,
    )


@router.delete(
    path="/{id}",
    name="bookss:delete-book-by-id",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_book(
    id: int,
    book_repo: BookCRUDRepository = fastapi.Depends(
        get_repository(repo_type=BookCRUDRepository)
    ),
) -> dict[str, str]:
    try:
        deletion_result = await book_repo.delete_book_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
