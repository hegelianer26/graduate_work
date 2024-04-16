from typing import Any, Dict, List, Optional

from db.storage import AbstractDataStorage
from elasticsearch import AsyncElasticsearch, NotFoundError


class ElasticService(AbstractDataStorage):
    """Интерфейс получения данных из Elastic"""

    def __init__(self, elastic: AsyncElasticsearch, index: str):
        self.index = index
        self.elastic = elastic

    async def _get_by_id(self, _id: str) -> Optional[Any]:
        """Получить данные из индекса по ID"""
        try:
            doc = await self.elastic.get(index=self.index, id=_id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def _search(
        self,
        query: Optional[Dict[Any, Any]] = None,
        from_: int = 0,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_how: Optional[str] = None,
    ) -> List[Any]:
        sort_how: str = "asc"
        if sort_by is not None and sort_by.startswith('-'):
            sort_how: str = "desc"
            sort_by = sort_by[1:]

        if query:
            query = {"query": query}
        if page_num and page_size:
            from_ = (int(page_num) - 1) * int(page_size)
        if sort_by and sort_how:
            sort = f"{sort_by}:{sort_how}"
        else:
            sort = None
        try:
            data = await self.elastic.search(
                index=self.index,
                body=query,
                from_=from_,
                size=page_size,
                sort=sort
            )
            hits = data.get("hits", {}).get("hits", [])
            result = [hit.get("_source") for hit in hits]
        except NotFoundError:
            return None
        return result

async def es_service():
    return ElasticService
