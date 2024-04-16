from pydantic_settings import BaseSettings, SettingsConfigDict


class FastapiConfig(BaseSettings):
    project_name: str
    movie_host: str
    movie_port: str
    session_key: str

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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix='fuzzy_',
        env_file_encoding='utf-8', extra='ignore')


fastapi_config = FastapiConfig()
redis_config = RedisConfig()
fasttext_config = FasttextConfig()
fuzz_config = FuzzyConfig()
