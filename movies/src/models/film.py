from typing import List, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):

    class Config:
        json_loads = orjson.loads 
        json_dumps = orjson_dumps


class Genre(BaseModel):
    uuid: str
    name: str


class Person(BaseModel):
    uuid: str
    full_name: str


class Movie(BaseOrjsonModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[Genre]]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]
    directors: Optional[List[Person]]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MovieSearch(BaseOrjsonModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]
    directors: Optional[List[Person]]
    duration: Optional[int]
    
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonFilmIds(BaseModel):
    uuid: str


class MoviePerson(BaseOrjsonModel):
    uuid: str
    full_name: str
    role: Optional[str]
    film_ids: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PersonDetail(BaseModel):
    uuid: str
    full_name: str
    role: str
    film_ids: str


class PersonFilm(BaseOrjsonModel):
    film: List[MovieSearch]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
