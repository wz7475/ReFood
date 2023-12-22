import logging
from time import sleep

import pika
from pika.exceptions import AMQPConnectionError
from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError
from config import ELASTIC_URL, RABBITHOST

def get_rabbitmq_connection(logger: logging.Logger):
    for i in range(10):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITHOST, heartbeat=0))
            return connection
        except AMQPConnectionError:
            sleep(5)
            logger.warning("Rabbitmq connection error, retrying in 5 seconds.")
    raise AMQPConnectionError("Cannot connect to rabbitmq")

def get_es_connection(logger: logging.Logger):
    for i in range(10):
        try:
            es = Elasticsearch(ELASTIC_URL)
            return es
        except ConnectionError:
            sleep(5)
            logger.warning("Elasticsearch connection error, retrying in 5 seconds.")
    raise Exception("Cannot connect to elasticsearch")
