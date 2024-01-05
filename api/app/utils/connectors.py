import logging
from time import sleep

import pika
from pika.exceptions import AMQPConnectionError
from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError
from .cfg import ELASTIC_URL, RABBITHOST, RECONNECT_INTERVAL_IN_S, AVAIBLE_RECONNECTS


connections = {}

def get_rabbitmq_connection(logger: logging.Logger):
    for i in range(AVAIBLE_RECONNECTS):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, heartbeat=0))
            return connection
        except AMQPConnectionError:
            logger.warning(f"Rabbitmq connection error, retrying in {RECONNECT_INTERVAL_IN_S} seconds.")
            sleep(RECONNECT_INTERVAL_IN_S)
    raise AMQPConnectionError("Cannot connect to rabbitmq")

def get_es_connection(logger: logging.Logger):
    for i in range(AVAIBLE_RECONNECTS):
        try:
            es = Elasticsearch(ELASTIC_URL)
            return es
        except ConnectionError:
            sleep(RECONNECT_INTERVAL_IN_S)
            logger.warning(f"Elasticsearch connection error, retrying in {RECONNECT_INTERVAL_IN_S} seconds.")
    raise Exception("Cannot connect to elasticsearch")
