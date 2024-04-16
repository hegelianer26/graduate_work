import asyncio

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(name='aiohttp_client', scope='session')
async def aiohttp_client_session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()
    print('session closed')


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_client):
    async def inner(url, params=None):
        return await aiohttp_client.get(url, params=params)
    return inner
