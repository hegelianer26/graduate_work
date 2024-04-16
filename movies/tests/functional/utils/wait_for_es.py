import backoff
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from tests_settings import elastic_config


@backoff.on_exception(backoff.expo,
                      ConnectionError)
def wait_for_es(es_client):
    return es_client.ping()

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=elastic_config.elastic_dsn)
    if wait_for_es(es_client):
        print('ES is ready')
