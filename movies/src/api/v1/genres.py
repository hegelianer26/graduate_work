from http import HTTPStatus
from typing import List

from core.auth_scheme import security_jwt
from fastapi import APIRouter, Depends, HTTPException
from models.film import Genre
from services.film import FilmService, get_film_service
from services.genre import GenreService, get_genre_service

from .dependencies import PaginateQueryParams as paginator

router = APIRouter()


@router.get(
    "/",
    response_model=List[Genre],
    summary="Жанры",
    description="Список доступных жанров",
    response_description="Название",
    tags=["Главная страница"],
)
async def get_genres(
    pagination: str = Depends(paginator),
    service: GenreService = Depends(get_genre_service),
    user: dict = Depends(security_jwt),
        ) -> List[Genre]:
    result = await service.get_genres(
        page_num=pagination.page_number, page_size=pagination.page_size)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return result


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Жанр",
    description="Информация по жанру",
    response_description="Информация об отдельном жанре",
    tags=["Страница жанра"],
)
async def get_one_genre(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    user: dict = Depends(security_jwt),
) -> Genre:
    result = await genre_service.get_one_genre(genre_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return result
