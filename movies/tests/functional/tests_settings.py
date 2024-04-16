from pydantic import Field
from pydantic_settings import BaseSettings


class ElasticConfig(BaseSettings):
    host: str = Field('elasticsearch', env="ELASTIC_HOST")
    port: int = Field('9200', env="ELASTIC_PORT")
    index_movies: str = Field('test_index', env="ELASTIC_TEST_INDEX_MOVIES_NAME")
    index_genres: str = Field('test_genres', env="ELASTIC_TEST_INDEX_GENRES_NAME")
    index_persons: str = Field('test_persons', env="ELASTIC_TEST_INDEX_PERSONS_NAME")

    @property
    def elastic_dsn(self):
        return f"http://{self.host}:{self.port}/"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


class RedisConfig(BaseSettings):
    REDIS_HOST: str = Field('127.0.0.1', env="REDIS_HOST")
    REDIS_PORT: int = Field('6379', env="REDIS_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


class ApiConfig(BaseSettings):
    API_HOST: str = Field('fastapi', env="API_HOST")
    API_PORT: int = Field('8080', env="API_PORT")

    @property
    def api_dsn(self):
        return f"http://{self.API_HOST}:{self.API_PORT}/"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

api_config = ApiConfig()
elastic_config = ElasticConfig()
redis_config = RedisConfig()
