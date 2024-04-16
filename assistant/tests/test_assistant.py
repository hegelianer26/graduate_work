from http import HTTPStatus
import pytest
import requests


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'кто снял фильм Терминатор'},
            {'status': HTTPStatus.OK}
        ),
        (
            {'text': 'сколько он снял фильмов'},
            {'status': HTTPStatus.OK}
        ),
        (
            {'text': 'сколько он длиться'},
            {'status': HTTPStatus.OK}
        ),
    ]
    )
def test_states(query_data, expected_answer):
    response = requests.post(
        'http://localhost:8092/duke_textual', json=query_data)
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'кто снял фильм Титаник'},
            {'status': HTTPStatus.OK, 'author': 'Джеймс Кэмерон'}
        ),
        (
            {'text': 'кто режиссер Довода'},
            {'status': HTTPStatus.OK, 'author': 'Кристофер Нолан'}
        ),
        (
            {'text': 'скажи кто создал фильм Я робот'},
            {'status': HTTPStatus.OK, 'author': 'Алекс Пройас'}
        ),
    ]
)
def test_movies(query_data, expected_answer):

    response = requests.post(
        'http://localhost:8092/duke_textual', json=query_data)
    response_text = response.json().get('response').get('text')

    assert expected_answer['author'] in response_text
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'сколько фильмов снял Джеймс Кэмерон'},
            {'status': HTTPStatus.OK, 'ammount': '5'}
        ),
        (
            {'text': 'количество фильмов у Кристофера Нолана'},
            {'status': HTTPStatus.OK, 'ammount': '9'}
        ),
        (
            {'text': 'как много фильмов у Алекса Пройаса'},
            {'status': HTTPStatus.OK, 'ammount': '3'}
        ),
    ]
)
def test_ammount(query_data, expected_answer):

    response = requests.post('http://localhost:8092/duke_textual', json=query_data)
    response_text = response.json().get('response').get('text')

    assert expected_answer['ammount'] in response_text
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'сколько длится Догма'},
            {'status': HTTPStatus.OK, 'ammount': '123'}
        ),
        (
            {'text': 'продолжительность Побега из Шоушенка'},
            {'status': HTTPStatus.OK, 'ammount': '142'}
        ),
        (
            {'text': 'сколько идет фильм Дурак'},
            {'status': HTTPStatus.OK, 'ammount': '116'}
        ),
    ]
)
def test_duration(query_data, expected_answer):

    response = requests.post('http://localhost:8092/duke_textual', json=query_data)
    response_text = response.json().get('response').get('text')

    assert expected_answer['ammount'] in response_text
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'помощь'},
            {'status': HTTPStatus.OK, 'scene': 'Help'}
        ),
        (
            {'text': 'как пользоваться'},
            {'status': HTTPStatus.OK, 'scene': 'Help'}
        ),
    ]
)
def test_help(query_data, expected_answer):

    response = requests.post('http://localhost:8092/duke_textual', json=query_data)
    response_scene = response.json().get('session_state').get('scene')

    assert response_scene == expected_answer['scene']
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'бла бла бла'},
            {'status': HTTPStatus.OK, 'scene': 'Error'}
        ),
        (
            {'text': 'есть ли жизнь на Марсе'},
            {'status': HTTPStatus.OK, 'scene': 'Error'}
        ),
    ]
)
def test_error(query_data, expected_answer):

    response = requests.post('http://localhost:8092/duke_textual', json=query_data)
    response_scene = response.json().get('session_state').get('scene')

    assert response_scene == expected_answer['scene']
    assert response.status_code == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'text': 'расскажи о себе'},
            {'status': HTTPStatus.OK, 'scene': 'Power'}
        ),
        (
            {'text': 'что ты умеешь'},
            {'status': HTTPStatus.OK, 'scene': 'Power'}
        ),
    ]
)
def test_power(query_data, expected_answer):

    response = requests.post('http://localhost:8092/duke_textual', json=query_data)
    response_scene = response.json().get('session_state').get('scene')

    assert response_scene == expected_answer['scene']
    assert response.status_code == expected_answer['status']
