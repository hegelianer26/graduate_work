from abc import ABC, abstractmethod
from db.redis import get_redis
from scenes.state import STATE_REQUEST_KEY
import json


class AbstractRequestParser(ABC):

    @property
    @abstractmethod
    def intents(self):
        pass

    @abstractmethod
    def get_movie(self, intent_name: str):
        pass

    @abstractmethod
    def get_author_name(self, intent_name: str):
        pass

    @abstractmethod
    def get_author_from_state(self):
        pass
    
    @abstractmethod
    def get_movie_from_state(self):
        pass

    @abstractmethod
    def get_intent_name(self):
        pass


class RequestParser(AbstractRequestParser):
    def __init__(self, request_body: str):
        self.request_body = request_body

    def __getitem__(self, key: str):
        return self.request_body[key]

    @property
    def intents(self):
        return self.request_body['request'].get('nlu', {}).get('intents', {})

    @property
    async def type(self):
        return self.request_body.get('request', {}).get('type')

    async def get_movie(self, intent_name: str):
        try:
            return self.intents[intent_name]['slots']['movie']['value']
        except KeyError:
            return []

    async def get_author_name(self, intent_name: str):
        if 'slots' in self.intents[intent_name] and 'author_name' in self.intents[intent_name]['slots']:
            author_last_name = self.intents[intent_name]['slots']['author_name']['value'].get('last_name', '')
            author_first_name = self.intents[intent_name]['slots']['author_name']['value'].get('first_name', '')
            author = author_first_name + ' ' + author_last_name

            return author

    async def get_author_from_state(self):
        author = self.request_body.get('state', {}).get(STATE_REQUEST_KEY, {}).get('author')

        return author

    async def get_movie_from_state(self):
        movie = self.request_body.get('state', {}).get(STATE_REQUEST_KEY, {}).get('movie')

        return movie

    async def get_intent_name(self):

        intent_name = next(iter(self.intents))

        return intent_name


class RequestParserDuke(AbstractRequestParser):

    def __init__(self, entities: str):
        self.entities = entities

    @property
    async def intents(self):
        return self.entities

    async def get_movie(self, intent_name: str):
        try:
            return self.entities['film_name']
        except IndexError:
            return []

    async def get_author_name(self, intent_name: str):
        try:
            return self.entities['author']
        except IndexError:
            return []

    async def get_intent_name(self):
        return self.entities['label']

    async def get_author_from_state(self):
        redis = await get_redis()

        session_id = self.entities.get('session_id')

        redis_states = await redis.get(session_id)

        if redis_states:
            redis_data = json.loads(redis_states)
            return redis_data.get('author')

    async def get_movie_from_state(self):
        redis = await get_redis()

        session_id = self.entities.get('session_id')

        redis_states = await redis.get(session_id)

        if redis_states:
            redis_data = json.loads(redis_states)
            return redis_data.get('movie')


async def get_request_parser_duke(intetns: str):
    return RequestParserDuke(intetns)
