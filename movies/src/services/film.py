import logging
from functools import lru_cache
from typing import List, Optional

from core.config import elastic_config
from db.elastic import get_elastic
from db.redis import get_redis
from db.storage import AbstractCacheStorage, AbstractDataStorage
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, HTTPException
from models.film import Movie, MovieSearch
from redis.asyncio import Redis
from services.base.elastic import ElasticService, es_service
from services.base.redis import RedisService, redis_service

FILM_CACHE_EXPIRE_IN_SECONDS = 50  # 60 * 5  # 5 минут
ELASTIC_INDEX_NAME = elastic_config.index_movies

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FilmService:

    def __init__(self,
                 cashe: AbstractCacheStorage,
                 search: AbstractDataStorage,
                 search_storage,
                 cashe_storage):

        self.cashe_storage = cashe_storage
        self.cashe = cashe(self.cashe_storage)
        self.search_storage = search_storage
        self.search = search(index=ELASTIC_INDEX_NAME, elastic=search_storage)

    # get_by_id возвращает объект фильма.
    # Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Movie]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        # film = await self._film_from_cache(film_id)
        key = f"get_by_id_{film_id}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)
        if not result:
            logger.info("данные по запросу отсутствуют в кэше")
            result = await self.search._get_by_id(film_id)
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")
        result = Movie(**result)

        return result

    async def get_films(
        self, sort: str, page: str, size: str, genre: str
    ) -> Optional[List[MovieSearch]]:

        key = f"get_films_sort{sort}_page{page}_size{size}_genre{genre}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)

        if sort not in ('-imdb_rating', 'imdb_rating'):
            raise HTTPException(
                status_code=422,
                detail="rating must be imdb_rating or -imdb_rating")

        if not result:
            if genre:
                query_body = {
                        "bool": {
                            "must": [
                                {"query_string": {
                                    "default_field": "genre_names", "query": genre}}
                                    ], }}
            else:
                query_body = {
                    "match_all": {}
                }
            logger.info("данные по запросу отсутствуют в кэше")
            result = await self.search._search(
                query=query_body,
                page_num=page,
                page_size=size,
                sort_by=sort,
            )
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")

        return result

    async def get_search(
        self, query: str, page: str, size: str
    ) -> Optional[List[MovieSearch]]:
        # from_ = (int(page) - 1) * int(page)
        # films = await self._films_from_cache(query + page + size)

        key = f"get_search_films_{query}_page{page}_size{size}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)

        if "!" in query:
            query = query.replace("!", "\\!")
        if ";" in query:
            query = query.replace(";", "\\;")

        if not result:
            logger.info("данные по запросу отсутствуют в кэше")
            query_body = {
                "bool": {"must": {"query_string": {"query": query}}},
            }
            result = await self.search._search(
                query=query_body,
                page_num=page,
                page_size=size,
            )
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")
        return result

    async def get_alike(
        self, genres: list, page: str, size: str
    ) -> Optional[List[MovieSearch]]:
        key = f"get_alike_films_genres{genres}_page{page}_size{size}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)

        genre_query = []
        for i in genres:
            genre_query.append(
                {"query_string": {"default_field": "genre_names", "query": i}})

        if not result:
            query_body = {"bool": {"should": genre_query}}
            logger.info("данные ", genre_query)
            result = await self.search._search(
                query=query_body,
                page_num=page,
                page_size=size,
            )
            logger.info("asfsadfsad", genres)
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")

        return result


@lru_cache()
def get_film_service(
    cashe: AbstractCacheStorage = Depends(redis_service),
    search: AbstractDataStorage = Depends(es_service),
    search_storage: AsyncElasticsearch = Depends(get_elastic),
    cashe_storage: Redis = Depends(get_redis),
) -> FilmService:
    return FilmService(
        cashe=cashe,
        cashe_storage=cashe_storage,
        search=search,
        search_storage=search_storage)
