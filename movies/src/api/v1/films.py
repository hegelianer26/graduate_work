from http import HTTPStatus
from typing import List, Union

from core.auth_scheme import security_jwt
from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import Genre, Movie, MovieSearch
from services.film import FilmService, get_film_service

from .dependencies import PaginateQueryParams as paginator

router = APIRouter()



@router.get(
    "/{film_id}",
    response_model=Movie,
    summary="Информация об отдельном фильме",
    description="Полная информация по фильму",
    response_description=f"Название, рейтинг, описание, жанры, актеры, "
    f"сценаристы и режиссер фильма",
    tags=["Страница фильма"],
)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
    user: dict = Depends(security_jwt),
) -> Movie:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    return Movie(
        uuid=film.uuid,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
        genre=film.genre,
    )


@router.get(
    "/{film_id}/alike",
    response_model=List[MovieSearch],
    summary="Похожие фильмы",
    description="Фильмы того же жанра",
    response_description="Название, рейтинг",
    tags=["Страница фильма"],
)
async def films_alike(
    film_id: str,
    pagination: str = Depends(paginator),
    film_service: FilmService = Depends(get_film_service),
    user: dict = Depends(security_jwt),
) -> List[MovieSearch]:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    genres = [genre.name for genre in film.genre]
    films = await film_service.get_alike(
        genres, pagination.page_number, pagination.page_size)
    return films


@router.get(
    "/search/",
    response_model=List[MovieSearch],
    summary="Поиск по фильмам",
    description="Поиск фильма по названию",
    response_description="Название, рейтинг",
    tags=["Поиск"],
)
async def film_search(
    query: str,
    pagination: str = Depends(paginator),
    film_service: FilmService = Depends(get_film_service),
) -> List[MovieSearch]:
    film = await film_service.get_search(
        query, pagination.page_number, pagination.page_size)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


@router.get(
    "/",
    response_model=List[MovieSearch],
    summary="Популярные фильмы",
    description=f"Популярные фильмы на основе рейтинга imdb "
    f"с возможностью фильтрации по жанрам",
    response_description="Название, рейтинг",
    tags=["Главная страница"],
)
async def get_films(
    pagination: str = Depends(paginator),
    sort: Union[str, None] = Query(default='-imdb_rating', enum=["imdb_rating", "-imdb_rating"]),
    genre: str = None,
    film_service: FilmService = Depends(get_film_service),
    user: dict = Depends(security_jwt),
) -> List[MovieSearch]:
    films = await film_service.get_films(   
        sort=sort, page=pagination.page_number,
        size=pagination.page_size,
        genre=genre
        )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return films
