from configs import elastic_setings, etl_settings
from decorators import backoff
from elasticsearch import Elasticsearch
from loggings import logger


class ElasticSearchConnection:
    start_sleep_time = etl_settings.start_sleep_time
    factor = etl_settings.factor
    border_sleep_time = etl_settings.border_sleep_time

    def __init__(self):
        self.my_connection = None
        self.ping = False
        self._connect()

    @backoff
    def _connect(self):
        self.my_connection = Elasticsearch(
            f'http://{elastic_setings.host}:{elastic_setings.port}')
        logger.info(
            'Соединение с Elasticsearch: %s', self.my_connection.ping())
        if not self.my_connection.ping():
            self.my_connection = Elasticsearch(
                f'http://{elastic_setings.host}:{elastic_setings.port}')
            raise ConnectionRefusedError

    @backoff
    def create_index(self, index, mappings, settings):
        if self.my_connection.indices.exists(index=index):
            pass
        else:
            self.my_connection.indices.create(
                index=index, settings=settings, mappings=mappings)
            logger.info('Индекс %s создан', index)

    @backoff
    def __del__(self):
        self.my_connection.close
        logger.info('Соединение с ElasticSearch закрыто')
