import os
from logging import StreamHandler, getLogger

from dotenv import load_dotenv

load_dotenv(dotenv_path='../django_api/.env')

level = os.environ.get('LOG_LEVEL')

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(level=level)
