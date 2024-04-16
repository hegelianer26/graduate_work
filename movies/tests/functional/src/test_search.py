from http import HTTPStatus

import pytest
from es_mapping import ES_SETTINGS, MAPPING_FOR_INDEX, MAPPING_FOR_PERSONS
from testdata.movies_data import data as movies_data
from testdata.persons_data import data as persons_data
from tests_settings import api_config, elastic_config

index_movies = elastic_config.index_movies
mappings_movies = MAPPING_FOR_INDEX
index_persons = elastic_config.index_persons
mappings_persons = MAPPING_FOR_PERSONS
settings = ES_SETTINGS
site = api_config.api_dsn


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Star Wars: Episode VI - Return of the Jedi',
                 'page_number': 1,
                 'page_size': 1},
                {'status': HTTPStatus.OK, 'length': 1, 'uuid': '025c58cd-1b7e-43be-9ffb-8571a613579b'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_movie_search(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(movies_data, index_movies), index_movies, mappings_movies, settings)
    # time.sleep(1)
    response = await make_get_request(
        url=f'{site}api/v1/films/search/', params=query_data)
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
                {'query': 'Alun Daviess',
                 'page_number': 1,
                 'page_size': 1},
                {'status': HTTPStatus.OK, 'length': 1, 'uuid': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_person_search(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(persons_data, index_persons), index_persons, mappings_persons, settings)

    response = await make_get_request(
        url=f'{site}api/v1/persons/search/', params=query_data)
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
                {'query': 'Alun Daviess',
                 'page_number': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ]
)
@pytest.mark.asyncio
async def test_validate_data_persons_search(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):

    await es_write_data(es_data(movies_data, index_movies), index_movies, mappings_movies, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/search/', params=query_data)
    async with response:
        status_code = response.status

    assert status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Star Wars: Episode VI - Return of the Jedi',
                 'page_number': -1},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY, }
        ),
        (
                {},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ]
)
@pytest.mark.asyncio
async def test_validate_data_movies_search(
        query_data, expected_answer, make_get_request, es_write_data, es_data: 'list[dict]'):
    await es_write_data(es_data(movies_data, index_movies), index_movies, mappings_movies, settings)

    response = await make_get_request(
        url=f'{site}api/v1/films/search/', params=query_data)
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'Alun Daviess',
                 'page_number': 1,
                 'page_size': 1},
                {'status': HTTPStatus.OK, 'length': 1, 'uuid': 'ffe0d805-3595-4cc2-a892-f2bedbec4ac6'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_person_search_cache(
        query_data, expected_answer, make_get_request, es_write_data, es_delete_data, es_data: 'list[dict]'):

    await es_write_data(es_data(persons_data, index_persons), index_persons, mappings_persons, settings)
    await es_delete_data(index_persons, doc=expected_answer["uuid"])
    response = await make_get_request(
        url=f'{site}api/v1/persons/search/', params=query_data)
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
                {'query': 'Star Wars: Episode VI - Return of the Jedi',
                 'page_number': 1,
                 'page_size': 1},
                {'status': HTTPStatus.OK, 'length': 1, 'uuid': '025c58cd-1b7e-43be-9ffb-8571a613579b'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_one_movie_search_cache(
        query_data, expected_answer, make_get_request, es_write_data, es_delete_data, es_data: 'list[dict]'):
    await es_write_data(es_data(movies_data, index_movies), index_movies, mappings_movies, settings)
    await es_delete_data(index_movies, doc=expected_answer["uuid"])

    response = await make_get_request(
        url=f'{site}api/v1/films/search/', params=query_data)
    async with response:
        status_code = response.status
        body = await response.json()

    assert status_code == expected_answer['status']
    assert len(body) == expected_answer['length']
    assert body[0]['uuid'] == expected_answer['uuid']
