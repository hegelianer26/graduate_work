import sys

sys.path
sys.path.append('/tests/')

from http import HTTPStatus

import pytest
from es_mapping import ES_SETTINGS, MAPPING_FOR_INDEX
from testdata.movies_data import data
from tests_settings import api_config, elastic_config

index = elastic_config.index_movies
mappings = MAPPING_FOR_INDEX
settings = ES_SETTINGS
site = api_config.api_dsn


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '025c58cd-1b7e-43be-9ffb-8571a613579b'},
                {'status': HTTPStatus.OK, 'length': 8}
        ),
        (
                {'query': 'NotReal'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_one_movie(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/{query_data["query"]}')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '025c58cd-1b7e-43be-9ffb-8571a613579b', 'page_number': 1, 'page_size': 5, },
                {'status': HTTPStatus.OK, 'length': 5}
        ),
    ]
)
@pytest.mark.asyncio
async def test_alike_movies(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/{query_data["query"]}/alike?page_number={query_data["page_number"]}&page_size={query_data["page_size"]}')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'page_number': 1, 'page_size': 100, 'sort': '-imdb_rating'},
            {'status': HTTPStatus.OK, 'length': 100, 'uuid': '025c58cd-1b7e-43be-9ffb-8571a613579b'}
        ),
        (
            {'page_number': 1, 'page_size': 2, 'sort': '-imdb_rating'},
            {'status': HTTPStatus.OK, 'length': 2, 'uuid': '025c58cd-1b7e-43be-9ffb-8571a613579b'}
        ),
        (
            {'page_number': 1, 'page_size': 1, 'sort': '-imdb_rating', 'genre': 'Action'},
            {'status': HTTPStatus.OK, 'length': 1, 'uuid': '025c58cd-1b7e-43be-9ffb-8571a613579b'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_all_movies(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/', params=query_data)
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']
    assert body[0]['uuid'] == expected_answer['uuid']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'page_number': -1},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
            {'sort': 123},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ]
)
@pytest.mark.asyncio
async def test_validate_data_movie(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/', params=query_data)
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '025c58cd-1b7e-43be-9ffb-8571a613579b'},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_movie_from_cache(
        query_data, expected_answer, make_get_request, es_write_data, es_delete_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)
    await make_get_request(url=f'{site}/api/v1/films/{query_data["query"]}')
    await es_delete_data(index, doc=query_data["query"])

    response = await make_get_request(
        url=f'{site}api/v1/films/{query_data["query"]}')
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']
