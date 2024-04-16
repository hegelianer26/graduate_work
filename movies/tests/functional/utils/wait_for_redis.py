import time

import backoff
import redis
from tests_settings import redis_config


@backoff.on_exception(backoff.expo,
                      redis.exceptions.ConnectionError,)
def wait_for_redis(redis_client):
    return redis_client.ping()


if __name__ == '__main__':
    redis_clent = redis.Redis(
        host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT)
    if wait_for_redis(redis_clent):
        print('Redis is ready')
