import inspect
import sys
from abc import ABC, abstractmethod
from typing import Optional
from loguru import logger
import aiohttp
import random

import scenes.intents as intents
from scenes.state import STATE_RESPONSE_KEY
from services.request_parsers import AbstractRequestParser
from core.config import fastapi_config
from .response_templates import (
    RESPONSE_TEMPLATES_AMMOUNT,
    RESPONSE_TEMPLATES_CREATOR,
    RESPONSE_TEMPLATES_COUNT,
    RESPONSE_TEMPLATES_ERROR,
    RESPONSE_TEMPLATES_POWER,
    RESPONSE_TEMPLATES_HELP,
    RESPONSE_TEMPLATES_WELCOME,
    RESPONSE_NOT_FOUND,
    RESPONSE_NOT_AUTHOR,
    RESPONSE_NOT_COUNT
    )


async def move_to_scene(request: AbstractRequestParser, intent_name: str):

    if intent_name == intents.GET_MOVIE_BY_AUTHOR:
        movie = await request.get_movie(intent_name)
        if movie is None or movie == []:
            movie = await request.get_movie_from_state()
        return Movie_author(movie)

    elif intent_name == intents.GET_MOVIE_COUNT:
        author = await request.get_author_name(intent_name)
        if author is None or author == []:
            author = await request.get_author_from_state()
        return Count_movies(author)

    elif intent_name == intents.GET_MOVIE_TIME:
        movie = await request.get_movie(intent_name)
        if movie is None or movie == []:
            movie = await request.get_movie_from_state()
        author = await request.get_author_from_state()

        return Movie_time(movie)

    elif intent_name == intents.HELP or intent_name == intents.GET_HELP:
        return Help()

    elif intent_name == intents.POWER or intent_name == intents.GET_POWER:
        return Power()

    elif intent_name == intents.ERROR or intent_name == {}:
        return Error()


class Scene(ABC):

    @classmethod
    def id(cls):
        return cls.__name__

    """Генерация ответа сцены"""
    @abstractmethod
    async def reply(self, request):
        raise NotImplementedError()

    """Проверка перехода к новой сцене"""
    async def move(self, request: AbstractRequestParser):
        next_scene = await self.handle_local_intents(request)
        if next_scene is None:
            next_scene = await self.handle_global_intents(request)
        return next_scene

    @abstractmethod
    async def handle_global_intents(self):
        raise NotImplementedError()

    @abstractmethod
    async def handle_local_intents(
            request: AbstractRequestParser) -> Optional[str]:
        raise NotImplementedError()

    async def fallback(self, request: AbstractRequestParser):
        selected_template = random.choice(RESPONSE_TEMPLATES_ERROR)
        return await self.make_response(text=selected_template)

    async def make_response(self, text, tts=None, state=None):
        response = {
            'text': text,
            'tts': tts if tts is not None else text,
        }

        webhook_response = {
            'response': response,
            'version': '1.0',
            STATE_RESPONSE_KEY: {
                'scene': self.id(),
            },
        }
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY].update(state)
        logger.info(webhook_response)
        return webhook_response


class MovieScene(Scene):

    async def handle_global_intents(self, request):
        intent_name = await request.get_intent_name()
        return await move_to_scene(request, intent_name)


class Welcome(MovieScene):
    async def reply(self, request: AbstractRequestParser):
        selected_template = random.choice(RESPONSE_TEMPLATES_WELCOME)
        return await self.make_response(text=selected_template)

    async def handle_local_intents(self, request: AbstractRequestParser):
        intent_name = await request.get_intent_name()
        return await move_to_scene(request, intent_name)


class Help(MovieScene):

    async def reply(self, request: AbstractRequestParser):
        selected_template = random.choice(RESPONSE_TEMPLATES_HELP)

        return await self.make_response(text=selected_template)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


class Movie_author(MovieScene):

    def __init__(self, movie):
        self.movie = movie

    async def reply(self, request: AbstractRequestParser):

        async with aiohttp.ClientSession() as session:

            url = f'http://{fastapi_config.movie_host}:{fastapi_config.movie_port}/api/v1/films/search/?query={self.movie}'
            async with session.get(url) as response:
                if response.status != 200:
                    selected_template = random.choice(
                        RESPONSE_NOT_FOUND)
                    return await self.make_response(text=selected_template)
                try:
                    data = await response.json()
                    author = data[0].get('directors')[0].get('full_name')
                    selected_template = random.choice(
                        RESPONSE_TEMPLATES_CREATOR).format(author=author)
                    return await self.make_response(
                        text=selected_template, state={'author': author,
                                                       'movie': self.movie})
                except IndexError:
                    selected_template = random.choice(
                        RESPONSE_NOT_AUTHOR)
                    return await self.make_response(text=selected_template)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


class Movie_time(MovieScene):

    def __init__(self, movie):
        self.movie = movie

    async def reply(self, request: AbstractRequestParser):
        async with aiohttp.ClientSession() as session:

            url = f'http://{fastapi_config.movie_host}:{fastapi_config.movie_port}/api/v1/films/search/?query={self.movie}'
            async with session.get(url) as response:
                if response.status != 200:
                    selected_template = random.choice(
                        RESPONSE_NOT_FOUND)
                    return await self.make_response(text=selected_template)
                try:
                    data = await response.json()
                    duration = data[0].get('duration')

                    selected_template = random.choice(
                        RESPONSE_TEMPLATES_COUNT).format(duration=duration)
                    return await self.make_response(
                        text=selected_template, state={'movie': self.movie})
                except IndexError:
                    selected_template = random.choice(
                        RESPONSE_NOT_COUNT)
                    return await self.make_response(text=selected_template)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


class Count_movies(MovieScene):

    def __init__(self, author):
        self.author = author

    async def reply(self, request: AbstractRequestParser):

        async with aiohttp.ClientSession() as session:

            url = f'http://{fastapi_config.movie_host}:{fastapi_config.movie_port}/api/v1/persons/search/?query={self.author}'
            async with session.get(url) as response:
                if response.status != 200:
                    selected_template = random.choice(RESPONSE_NOT_FOUND)
                    return await self.make_response(text=selected_template)

                data = await response.json()
                ids = data[0].get('film_ids')
                ids_list = ids.split(", ")
                ammount = len(ids_list)

            if ammount is None or ammount == 0:
                selected_template = random.choice(RESPONSE_NOT_COUNT)
                return await self.make_response(text=selected_template)

            selected_template = random.choice(
                RESPONSE_TEMPLATES_AMMOUNT).format(ammount=ammount)
            return await self.make_response(
                text=selected_template,
                state={'author': self.author},)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


class Power(MovieScene):
    async def reply(self, request: AbstractRequestParser):
        selected_template = random.choice(RESPONSE_TEMPLATES_POWER)
        return await self.make_response(
            text=selected_template)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


class Error(MovieScene):
    async def reply(self, request: AbstractRequestParser):
        return await self.fallback(request)

    async def handle_local_intents(self, request: AbstractRequestParser):
        pass


def _list_scenes():
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES = {
    scene.id(): scene for scene in _list_scenes()
}

DEFAULT_SCENE = Welcome
ERROR_SCENE = Error
