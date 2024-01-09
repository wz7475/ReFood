import json
import logging
from time import sleep

import pika
from elasticsearch import Elasticsearch, ConnectionError
from logger import get_logger
from es_tools import create_index, index_document, delete_indexed_document
from cfg import OFFER_INDEX, ADD_OFFER_QUEUE, DELETE_OFFER_QUEUE, ELASTIC_URL, RABBITHOST, RECONNECT_INTERVAL_IN_S, \
    AVAIBLE_RECONNECTS

logger = get_logger()


def add_callback(ch, method, properties, body):
    """
    expected body: document to index with field "id" and fields with data
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    document = json.loads(body)
    document_id = document["id"]
    document.pop("id")
    logger.info(document)
    index_document(es, OFFER_INDEX, document, document_id)
    logger.info(f"Added document: {document_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def delete_callback(ch, method, properties, body):
    """
    expected body: field "id" with id of document to delete, other fields are ignored
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    document = json.loads(body)
    document_id = document["id"]
    delete_indexed_document(es, OFFER_INDEX, document_id)
    logger.info(f"Deleted document: {document_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def get_es_connection(index_name, logger: logging.Logger):
    for i in range(AVAIBLE_RECONNECTS):
        try:
            es = Elasticsearch(ELASTIC_URL)
            create_index(es, index_name, logger)
        except ConnectionError:
            logger.warning(f"Elasticsearch connection error, retrying in {RECONNECT_INTERVAL_IN_S} seconds.")
            sleep(RECONNECT_INTERVAL_IN_S)
            continue
        return es
    raise ConnectionError("Elasticsearch connection error.")


if __name__ == '__main__':


    # elasticsearch
    es = get_es_connection(OFFER_INDEX, logger)

    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITHOST, heartbeat=0)
    )
    channel = connection.channel()

    channel.queue_declare(queue=ADD_OFFER_QUEUE)
    channel.queue_declare(queue=DELETE_OFFER_QUEUE)
    channel.basic_consume(queue=ADD_OFFER_QUEUE, on_message_callback=add_callback, auto_ack=False)
    channel.basic_consume(queue=DELETE_OFFER_QUEUE, on_message_callback=delete_callback, auto_ack=False)

    channel.start_consuming()
