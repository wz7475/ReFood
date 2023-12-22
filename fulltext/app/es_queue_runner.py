import json
import logging
from time import sleep

import pika
import argparse
from elasticsearch import Elasticsearch
from logger import get_logger
from es_tools import create_index, index_document, delete_indexed_document
from config import OFFER_INDEX, ADD_OFFER_QUEUE, UPDATE_OFFER_QUEUE, DELETE_OFFER_QUEUE
from elasticsearch import ConnectionError
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
    for i in range(10):
        try:
            es = Elasticsearch("http://elasticsearch:9200")
            create_index(es, index_name, logger)
        except ConnectionError:
            logger.warning("Elasticsearch connection error, retrying in 5 seconds.")
            sleep(5)
            continue
        return es
    raise ConnectionError("Elasticsearch connection error.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, choices=["add", "delete"], required=True)
    args = parser.parse_args()
    if args.mode == "add":
        callback = add_callback
        queue = ADD_OFFER_QUEUE
    elif args.mode == "delete":
        callback = delete_callback
        queue = DELETE_OFFER_QUEUE
    else:
        raise ValueError("Invalid mode.")

    # elasticsearch
    es = get_es_connection(OFFER_INDEX, logger)

    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
