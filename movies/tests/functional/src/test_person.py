from http import HTTPStatus

import pytest
from es_mapping import ES_SETTINGS, MAPPING_FOR_PERSONS
from testdata.persons_data import data
from tests_settings import api_config, elastic_config

index = elastic_config.index_persons
mappings = MAPPING_FOR_PERSONS
settings = ES_SETTINGS
site = api_config.api_dsn

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'},
                {'status': HTTPStatus.OK, 'length': 4}
        ),
        (
                {'query': 'NotReal'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_one_person(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/{query_data["query"]}')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
                {'query': 'NotReal'},
                {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_film_person(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/{query_data["query"]}/film')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'},
                {'status': HTTPStatus.OK, 'length': 4}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_person(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/{query_data["query"]}')
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (       
            {'page_number': 1, 'page_size': 100},
            {'status': HTTPStatus.OK, 'length': 100}
        ),
        (
            {'page_number': 2, 'page_size': 60},
            {'status': HTTPStatus.OK, 'length': 40}
        ),
        (
            {},
            {'status': HTTPStatus.OK, 'length': 50}
        ),
        (
            {'page_number': 3, 'page_size': 100},
            {'status': HTTPStatus.NOT_FOUND, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_all_persons(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/', params=query_data)
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
async def test_validate_data_person(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/', params=query_data)
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'},
                {'status': HTTPStatus.OK, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_genre_from_cache(
        query_data, expected_answer,
        make_get_request, es_write_data,
        es_delete_data, es_data: 'list[dict]'):

    await es_write_data(es_data(data, index), index, mappings, settings)
    await make_get_request(url=f'{site}api/v1/persons/{query_data["query"]}')
    await es_delete_data(index, doc=query_data["query"])

    response = await make_get_request(
        url=f'{site}api/v1/persons/{query_data["query"]}')
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']
