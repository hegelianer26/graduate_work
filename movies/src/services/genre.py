import logging
from functools import lru_cache
from typing import List, Optional

from core.config import elastic_config
from db.elastic import get_elastic
from db.redis import get_redis
from db.storage import AbstractCacheStorage, AbstractDataStorage
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Genre
from redis.asyncio import Redis
from services.base.elastic import ElasticService, es_service
from services.base.redis import RedisService, redis_service

CACHE_EXPIRE_IN_SECONDS = 50  # 60 * 5  # 5 минут
ELASTIC_INDEX_NAME = elastic_config.index_genres


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GenreService:
    def __init__(self,
                 cashe: AbstractCacheStorage,
                 search: AbstractDataStorage,
                 search_storage,
                 cashe_storage):

        self.cashe_storage = cashe_storage
        self.cashe = cashe(self.cashe_storage)
        self.search_storage = search_storage
        self.search = search(index=ELASTIC_INDEX_NAME, elastic=search_storage)

    async def get_genres(
            self, page_num: int, page_size: int) -> Optional[List[Genre]]:
        key = f"get_genres_page{page_num}_size{page_size}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)
        if not result:
            logger.info("данные по запросу отсутсвуют в кэше")
            result = await self.search._search(
                query={"match_all": {}},
                page_num=page_num,
                page_size=page_size,
            )
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")
        result = [Genre(**item) for item in result]
        return result

    async def get_one_genre(self, genre_id: str) -> Genre:
        key = f"get_one_genre_id_{genre_id}"
        result = await self.cashe._get_from_cache(key=key, use_pickle=True)
        if not result:
            logger.info("данные по запросу отсутсвуют в кэше")
            result = await self.search._get_by_id(genre_id)
            if not result:
                logger.info("данные по запросу не найдены в индексе")
                return None
            await self.cashe._put_to_cache(
                key=key,
                value=result,
                cache_expire=CACHE_EXPIRE_IN_SECONDS,
                use_pickle=True,
            )
            logger.info("данные добавлены в кэш")
        else:
            logger.info("данные загружены из кэша")
        result = Genre(**result)
        return result


@lru_cache()
def get_genre_service(
    cashe: AbstractCacheStorage = Depends(redis_service),
    search: AbstractDataStorage = Depends(es_service),
    search_storage: AsyncElasticsearch = Depends(get_elastic),
    cashe_storage: Redis = Depends(get_redis),
) -> GenreService:
    return GenreService(
        cashe=cashe,
        cashe_storage=cashe_storage,
        search=search,
        search_storage=search_storage)
