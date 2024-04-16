
import psycopg2
import psycopg2.extras
from configs import etl_settings, postgres_settings
from decorators import backoff
from loggings import logger


class PostgresConnection:
    start_sleep_time = etl_settings.start_sleep_time
    factor = etl_settings.factor
    border_sleep_time = etl_settings.border_sleep_time

    def __init__(self):
        self.my_connection = None
        self.my_cursor = None
        self.params = None
        self._connect()

    @backoff
    def _connect(self):
        self.my_connection = psycopg2.connect(**postgres_settings.dict())
        self.my_cursor = self.my_connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        logger.info("Подключились к postgres")

    @backoff
    def extract_data(self, sql_statement, updated, size):
        self.my_cursor.execute(sql_statement.format(upd=updated))
        result = self.my_cursor.fetchmany(size=size)
        if result:
            return result
        return None

    @backoff
    def __del__(self):
        for c in (self.my_cursor, self.my_connection):
            try:
                c.close()
            except:
                pass
        logger.info("Закрыли соединение c postgres и курсор ")
