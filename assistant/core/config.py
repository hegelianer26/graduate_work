from pydantic_settings import BaseSettings, SettingsConfigDict


class FastapiConfig(BaseSettings):
    project_name: str
    project_host: str
    project_port: str
    project_protocol: str
    movie_host: str
    movie_port: str
    movie_protocol: str
    session_key: str

    @property
    def movie_url(self):
        return f'{self.movie_protocol}://{self.movie_host}:{self.movie_port}'

    @property
    def assistant_url(self) -> str:
        return f'{self.project_protocol}://{self.project_host}:{self.project_port}'

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='fastapi_',
        env_file_encoding='utf-8', extra='ignore')


class FasttextConfig(BaseSettings):
    threshold: float
    intents_file: str
    lr: float
    epoch: int
    wordNgrams: int

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='fasttext_',
        env_file_encoding='utf-8', extra='ignore')


class RedisConfig(BaseSettings):
    host: str
    port: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='redis_',
        env_file_encoding='utf-8', extra='ignore')


class FuzzyConfig(BaseSettings):
    threshold: int
    movie_list_file: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='fuzzy_',
        env_file_encoding='utf-8', extra='ignore')


class PostgresConfig(BaseSettings):

    host: str
    user: str
    password: str
    dbname: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='postgres_',
        env_file_encoding='utf-8', extra='ignore')


fastapi_config = FastapiConfig()
redis_config = RedisConfig()
fasttext_config = FasttextConfig()
fuzz_config = FuzzyConfig()
postgres_config = PostgresConfig()
