from http import HTTPStatus
from typing import List

from core.auth_scheme import security_jwt
from fastapi import APIRouter, Depends, HTTPException
from models.film import (MoviePerson, MovieSearch, Person, PersonDetail,
                         PersonFilm)
from services.person import PersonService, get_person_service

from .dependencies import PaginateQueryParams as paginator

router = APIRouter()


@router.get(
    "/search",
    response_model=List[MoviePerson],
    summary="Поиск по персонам",
    description="Поиск персон по имени",
    response_description="Список найденых персон",
    tags=["Поиск"],
)
async def get_search(
    query: str,
    pagination: str = Depends(paginator),
    person_service: PersonService = Depends(get_person_service),
) -> List[MoviePerson]:
    result = await person_service.get_search(
        query, pagination.page_number, pagination.page_size)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return result


@router.get(
    "/{person_id}",
    response_model=PersonDetail,
    summary="Страница персонажа",
    description="Данные по персоне",
    response_description="Имя, список фильмов с участием, роли",
    tags=["Страница персонажа"],
)
async def get_one_person(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    user: dict = Depends(security_jwt),
) -> PersonDetail:
    result = await person_service.get_one_person(person_id)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return result


@router.get(
    "/",
    response_model=List[Person],
    summary="Персоны",
    description="Список всех персон",
    response_description="ФИО, uuid",
    tags=["Главная страница"],
)
async def get_persons(
    pagination: str = Depends(paginator),
    service: PersonService = Depends(get_person_service),
    user: dict = Depends(security_jwt),
) -> List[Person]:
    result = await service.get_persons(
        page_num=pagination.page_number, page_size=pagination.page_size)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return result


@router.get(
    "/{person_id}/film",
    response_model=List[MovieSearch],
    summary="Страница персонажа",
    description="Фильмы по персоне",
    response_description="Название, рейтинг",
    tags=["Страница персонажа"],
)
async def get_person_service(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> MovieSearch:
    result = await person_service.get_one_person(person_id)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person films not found")
    return result.film
