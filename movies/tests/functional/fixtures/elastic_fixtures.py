import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from tests_settings import elastic_config


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(hosts=elastic_config.elastic_dsn, verify_certs=False)
    yield es_client
    # await delete
    await es_client.close()


@pytest_asyncio.fixture(name='es_data')
def es_data():
    def inner(es_data, index):
        bulk_query: list[dict] = []
        for row in es_data:
            data = {'_index': index, '_id': row['uuid']}
            data.update({'_source': row})
            bulk_query.append(data)
        return bulk_query
    return inner


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(data: 'list[dict]', index, mappings, settings):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(
            index=index, mappings=mappings, settings=settings)

        updated, errors = await async_bulk(client=es_client, actions=data, refresh=True)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(name='es_delete_data')
def es_delete_data(es_client):
    async def inner(index, doc):
        if await es_client.indices.exists(index=index):
            await es_client.delete(index=index, id=doc)
    return inner
