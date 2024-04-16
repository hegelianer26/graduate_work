
import psycopg2
import psycopg2.extras
from decorators import backoff
from loggings import logger

# from configs import postgres_settings, etl_settings


class PostgresConnection:
    # start_sleep_time = etl_settings.start_sleep_time
    # factor = etl_settings.factor
    # border_sleep_time = etl_settings.border_sleep_time
    start_sleep_time = 1
    factor = 1
    border_sleep_time = 1

    def __init__(self):
        self.my_connection = None
        self.my_cursor = None
        self.params = None
        self._connect()

    @backoff
    def _connect(self):
        # self.my_connection = psycopg2.connect(**postgres_settings.dict())
        self.my_connection = psycopg2.connect(**dsn)
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


from datetime import datetime

from sql_queries import big_sql_query
from states import JsonFileStorage, State

my_storage = State(
        JsonFileStorage(file_path='/home/art/middle/new_admin_panel_sprint_3/etl/states.json'))
dsn = {
    'dbname': 'postgres_1',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432,
    # 'options': '-c search_path=content',
}

def get_time():
    time_dirty = my_storage.get_state('Movies')
    time = datetime.strptime(time_dirty, "%Y-%m-%d %H:%M:%S.%f%z")
    return time

q = PostgresConnection()
state_time = get_time()
r = q.extract_data(big_sql_query, get_time(), 10)



if r: 
    sql_time = r[0]['great']

    print(len(r))
    print(state_time)
    print(r)

    print(sql_time)
    print(state_time, '>', sql_time, state_time>sql_time)