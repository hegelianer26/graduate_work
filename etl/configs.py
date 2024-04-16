from pydantic import BaseSettings, Field


class PostgresConfig(BaseSettings):

    host: str = Field(..., env="DB_HOST")
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    dbname: str = Field(..., env="DB_NAME")
    port: int = Field(..., env="DB_PORT")
    # options: str = Field(..., env="DB_options")

    class Config:
        env_file = "../django_api/.env"
        env_file_encoding = 'utf-8'

    @property
    def postgresql_url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class ElasticConfig(BaseSettings):
    host: str = Field(env="ELASTIC_HOST")
    port: int = Field(env="ELASTIC_PORT")
    index_movies: str = Field('index', env="ELASTIC_INDEX_MOVIES_NAME")
    index_genres: str = Field('genres', env="ELASTIC_INDEX_GENRES_NAME")
    index_persons: str = Field('persons', env="ELASTIC_INDEX_PERSONS_NAME")

    @property
    def elastic_dsn(self):
        return f"http://{self.host}:{self.port}/"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


class ETLConfig(BaseSettings):
    start_sleep_time = 0.1
    factor = 2
    border_sleep_time = 10
    storage_file_path = 'states.json'
    batch_size = 5000
    timer = 20.0


class RedisConfig(BaseSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")

    class Config:
        env_file = "../django_api/.env"
        env_file_encoding = 'utf-8'

    # REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1") str = Field(env="REDIS_HOST")
    # REDIS_PORT = int(os.getenv("REDIS_PORT", 6379)) int = Field(env="REDIS_PORT")

postgres_settings = PostgresConfig()
elastic_setings = ElasticConfig()
etl_settings = ETLConfig()
redis_config = RedisConfig()
