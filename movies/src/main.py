import logging
import time

import uvicorn
from api.v1 import films, genres, persons
from core.config import elastic_config, fastapi_config, redis_config
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = FastAPI(
    title=fastapi_config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = Redis(
        host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT)
    elastic.es = AsyncElasticsearch(
        hosts=[elastic_config.elastic_dsn]
    )


# проверка времени ответа
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time
    logger.info(
        "Time took to process the request and return response is %4.2f sec",
        response_time,
    )
    return response


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films")
app.include_router(genres.router, prefix="/api/v1/genres")
app.include_router(persons.router, prefix="/api/v1/persons")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
