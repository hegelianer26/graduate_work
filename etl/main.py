from datetime import datetime
from threading import Timer

import redis
from configs import elastic_setings, etl_settings, redis_config
from elastic_to import ElasticSearchConnection
from elasticsearch.helpers import streaming_bulk
from loggings import logger
from mappings import (ES_SETTINGS, MAPPING_FOR_GENRES, MAPPING_FOR_INDEX,
                      MAPPING_FOR_PERSONS)
from postgres_from import PostgresConnection
from sql_queries import (big_sql_query, genre_sql_query, person_sql_query,
                         small_genre_query, small_movie_query,
                         small_person_query)
from states import JsonFileStorage, State

r = redis.Redis(host=redis_config.REDIS_HOST, port=redis_config.REDIS_PORT)


def get_time(index):
    # time_dirty = my_storage.get_state('Movies')
    # time = datetime.strptime(time_dirty, "%Y-%m-%d %H:%M:%S.%f%z")
    time_dirty = r.get(name=index)
    if time_dirty is not None:
        # time = datetime.strptime(
        #     time_dirty.decode('utf-8'), "%Y-%m-%d %H:%M:%S.%f%z")
        time = datetime.strptime(time_dirty.decode('utf-8'), "%Y-%m-%d %H:%M:%S.%f")

    else:
        time = datetime.strptime(
            "0001-01-01 00:00:00.000000+0000", "%Y-%m-%d %H:%M:%S.%f%z")
    return time


def set_time(time_object, index):
    dt_str = time_object.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    # my_storage.set_state('Movies', dt_str)
    # time = r.set(name=index, value=dt_str)
    r.set(name=index, value=dt_str)


def check_needs(db,  query, index):
    updated = get_time(index)
    data = db.extract_data(query, updated, 1)
    for i in data:
        return i[0]


def extract(db, query, index):
    updated = get_time(index)
    logger.info(updated)
    data = db.extract_data(query, updated, etl_settings.batch_size)
    if data:
        logger.info('Выгружено %d фильмов', len(data))
        logger.info('Выгружено %s', data)
    return data


def transform(data, index):
    if index == 'index' or index == 'index_new':
        for row in data:
            print('asdfasd', row["duration"],)
            doc = {
                "_id": row["uuid"],
                "uuid": row["uuid"],
                "imdb_rating": row["imdb_rating"],
                "genre_names": row["genre_names"],
                "genre": row["genre"],
                "title": row["title"],
                "description": row["description"],
                "director_name": row["director_name"],
                "actors_names": [row["actors_names"]],
                "writers_names": [row["writers_names"]],
                "actors": row["actors"],
                "writers": row["writers"],
                "directors": row["directors"],
                "duration": row["duration"],
            }
            yield doc
    elif index == 'genres' or index == 'genres_new':
        for row in data:
                doc = {
                    "_id": row["uuid"],
                    "uuid": row["uuid"],
                    "name": row["name"],
                }
                yield doc
    elif index == 'persons' or index == 'persons_new':
        for row in data:
                doc = {
                    "_id": row["uuid"],
                    "uuid": row["uuid"],
                    "film_ids": row["film_ids"],
                    "full_name": row["full_name"],
                    "role": row["role"],
                    "film": row["film"],
                }
                yield doc


def load(data, index, mappings, settings):
    successes = 0
    if data:
        elastic = ElasticSearchConnection()
        elastic.create_index(index, mappings, settings)
        for ok, action in streaming_bulk(client=elastic.my_connection,
                                         index=index,
                                         actions=transform(data, index)
                                         ):
            successes += ok
            logger.info("Indexed %d documents" % (successes))
        # if index == 'index':
        set_time(time_object=data[0]['great'], index=index)

    else:
        logger.info(
            'Elasticseach в актуальном состоянии, загрузки не требуются')


if __name__ == '__main__':

    my_storage = State(
        JsonFileStorage(file_path=etl_settings.storage_file_path))

    def f():
        logger.info('начало etl')
        db = PostgresConnection()
        indexex = {
             'index': [
                  big_sql_query, elastic_setings.index_movies,
                  MAPPING_FOR_INDEX, small_movie_query],
             'genres': [
                  genre_sql_query, elastic_setings.index_genres,
                  MAPPING_FOR_GENRES, small_genre_query],
             'persons': [
                  person_sql_query, elastic_setings.index_persons,
                  MAPPING_FOR_PERSONS, small_person_query],
                  }

        Timer(etl_settings.timer, f).start()
        idx = {}
        for k, v in indexex.items():
            if check_needs(db, v[3], v[1]) > get_time(index=v[1]).replace(tzinfo=None):
                idx[k] = v
        if len(idx) > 0:
            for i in idx:
                logger.info('начало загрузки')
                data = extract(db, query=idx[i][0], index=idx[i][1])
                if data:
                    load(
                        data, index=idx[i][1], mappings=idx[i][2],
                        settings=ES_SETTINGS)

        else:
            logger.info(
                'Elasticseach в актуальном состоянии, обновлений не найдено')
            logger.info('завершение etl')
    f()
