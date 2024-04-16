import pickle
from typing import Any, Generic, Optional, Type, TypeVar

from db.storage import AbstractCacheStorage
from pydantic import BaseModel
from redis.asyncio import Redis


class RedisService(AbstractCacheStorage):
    """Интерфейс взаимодействия с Redis"""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def _get_from_cache(
        self, key: str, use_pickle: bool = False
    ) -> Optional[Any]:
        data = await self.redis.get(f"fastapi:functions_and_params:{key}")
        if not data:
            return None
        if use_pickle:
            data = pickle.loads(data)
        return data

    async def _put_to_cache(
        self, key: str, value: Any, cache_expire: int, use_pickle: bool = False
    ):
        if use_pickle:
            value = pickle.dumps(value)
        structured_key = f"fastapi:functions_and_params:{key}"
        await self.redis.set(name=structured_key, value=value, ex=cache_expire)


async def redis_service():
    return RedisService
