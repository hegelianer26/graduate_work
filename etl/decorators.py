import time
from functools import wraps

from loggings import logger

EXECUTION_ERROR = "Произошла ошибка при выполнении функции {name}: {error}."


def backoff(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        cls = args[0]
        sleep_time = cls.start_sleep_time
        while True:
            try:
                return fn(*args, **kw)
            except Exception as error:
                logger.error(
                    EXECUTION_ERROR.format(name=fn.__name__, error=error))
                if sleep_time < cls.border_sleep_time:
                    sleep_time += cls.start_sleep_time * (2**cls.factor)
                else:
                    sleep_time = cls.border_sleep_time
                time.sleep(sleep_time)
                logger.info(sleep_time)

    return wrapper
