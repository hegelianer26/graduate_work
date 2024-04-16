from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)


class ElasticConfig(BaseSettings):
    host: str = Field(env="ELASTIC_HOST")
    port: int = Field(env="ELASTIC_PORT")
    index_movies: str = Field(env="ELASTIC_INDEX_MOVIES_NAME")
    index_genres: str = Field(env="ELASTIC_INDEX_GENRES_NAME")
    index_persons: str = Field(env="ELASTIC_INDEX_PERSONS_NAME")

    @property
    def elastic_dsn(self):
        return f"http://{self.host}:{self.port}/"

    class Config:
        env_file = ".env_elastic"
        env_file_encoding = 'utf-8'


class FastapiConfig(BaseSettings):
    PROJECT_NAME: str = Field(env="fastapi_project_name")
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(env="ALGORITHM")

    class Config:
        env_file = ".env_movies"
        env_file_encoding = 'utf-8'


class RedisConfig(BaseSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")

    class Config:
        env_file = ".env_redis"
        env_file_encoding = 'utf-8'


elastic_config = ElasticConfig()
redis_config = RedisConfig()
fastapi_config = FastapiConfig()