
import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis
from loguru import logger
from contextlib import asynccontextmanager

from core.config import fastapi_config, redis_config
from db import redis
from api.v1 import bot

from starlette.middleware.sessions import SessionMiddleware


logger.add(
    'logs/assistant.json',
    format='{time} {level} {message}',
    level='INFO',
    rotation='1 week',
    serialize=True)

redis_host = redis_config.host
redis_port = redis_config.port
redis.redis = Redis(decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis.redis
    yield


app = FastAPI(title=fastapi_config.project_name, lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

app.include_router(bot.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8092,
        reload=True
    )
