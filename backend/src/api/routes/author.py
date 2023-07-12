import fastapi
import pydantic

from src.api.dependencies.repository import get_repository
from src.models.schemas.author import (
    AuthorInCreate,
    AuthorInResponse,
    AuthorInUpdate,
)
from src.repository.crud.author import AuthorCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)

router = fastapi.APIRouter(prefix="/authors", tags=["authors"])


@router.post(
    path="",
    name="authorss:create-authors",
    response_model=AuthorInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_author(
    author_create: AuthorInCreate,
    author_repo: AuthorCRUDRepository = fastapi.Depends(
        get_repository(repo_type=AuthorCRUDRepository)
    ),
) -> AuthorInResponse:
    db_author = await author_repo.create_author(author_create)

    return AuthorInResponse(id=db_author.id, name=db_author.name)


@router.get(
    path="",
    name="authorss:read-authors",
    response_model=list[AuthorInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_authors(
    author_repo: AuthorCRUDRepository = fastapi.Depends(
        get_repository(repo_type=AuthorCRUDRepository)
    ),
) -> list[AuthorInResponse]:
    db_authors = await author_repo.read_authors()
    db_author_responses = [
        AuthorInResponse(id=author.id, name=author.name) for author in db_authors
    ]
    return db_author_responses


@router.get(
    path="/{id}",
    name="authorss:read-author-by-id",
    response_model=AuthorInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_author(
    id: int,
    author_repo: AuthorCRUDRepository = fastapi.Depends(
        get_repository(repo_type=AuthorCRUDRepository)
    ),
) -> AuthorInResponse:
    try:
        db_author = await author_repo.read_author_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return AuthorInResponse(id=db_author.id, name=db_author.name)


@router.patch(
    path="/{id}",
    name="authorss:update-author-by-id",
    response_model=AuthorInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_author(
    id: int,
    author_update: AuthorInUpdate,
    author_repo: AuthorCRUDRepository = fastapi.Depends(
        get_repository(repo_type=AuthorCRUDRepository)
    ),
) -> AuthorInResponse:
    author_update = AuthorInUpdate(
        name=author_update.name,
    )
    try:
        updated_db_author = await author_repo.update_author_by_id(
            id=id, author_update=author_update
        )

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return AuthorInResponse(id=updated_db_author.id, name=updated_db_author.name)


@router.delete(
    path="/{id}",
    name="authorss:delete-author-by-id",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_author(
    id: int,
    author_repo: AuthorCRUDRepository = fastapi.Depends(
        get_repository(repo_type=AuthorCRUDRepository)
    ),
) -> dict[str, str]:
    try:
        deletion_result = await author_repo.delete_author_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
