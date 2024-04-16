from abc import ABC, abstractmethod


class AbstractDataStorage(ABC):
    @abstractmethod
    async def _get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _search(self, *args, **kwargs):
        pass


class AbstractCacheStorage(ABC):

    @abstractmethod
    async def _get_from_cache(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _put_to_cache(self, *args, **kwargs):
        pass
