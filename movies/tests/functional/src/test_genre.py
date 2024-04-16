from http import HTTPStatus

import pytest
from es_mapping import ES_SETTINGS, MAPPING_FOR_GENRES
from testdata.genres_data import data
from tests_settings import api_config, elastic_config

index = elastic_config.index_genres
mappings = MAPPING_FOR_GENRES
settings = ES_SETTINGS
site = api_config.api_dsn


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '9c627155-d6dc-432c-bdd0-09030aefdb8c'},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
                {'query': 'NotReal'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_one_genre(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/genres/{query_data["query"]}')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (       
            {'page_number': 1, 'page_size': 400},
            {'status': HTTPStatus.OK, 'length': 400}
        ),
        (
            {'page_number': 2, 'page_size': 300},
            {'status': HTTPStatus.OK, 'length': 300}
        ),
        (
            {},
            {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
            {'page_number': 3, 'page_size': 500},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_all_genres(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/genres/', params=query_data)
    async with response:
        status_code = response.status
        body = await response.json()
    
    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']



@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (       
            {'page_number': -1},
            {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ]
)
@pytest.mark.asyncio
async def test_validate_data_genre(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/genres/', params=query_data)
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': '9c627155-d6dc-432c-bdd0-09030aefdb8c'},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_genre_from_cache(
        query_data, expected_answer, make_get_request, es_write_data, es_delete_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)
    await make_get_request(url=f'{site}api/v1/genres/{query_data["query"]}')
    await es_delete_data(index, doc=query_data["query"])

    response = await make_get_request(
        url=f'{site}api/v1/genres/{query_data["query"]}')
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']