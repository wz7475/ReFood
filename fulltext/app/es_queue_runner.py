import json
from time import sleep

import pika
import argparse
from elasticsearch import Elasticsearch
from logger import get_logger
from es_tools import es_queue_on_index, index_document, delete_indexed_document, update_indexed_document
from config import OFFER_INDEX, ADD_OFFER_QUEUE, UPDATE_OFFER_QUEUE, DELETE_OFFER_QUEUE

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


def update_callback(ch, method, properties, body):
    """
    expected body: document to update with field "id" and fields with data to update
    data not present in body is not updated
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    document = json.loads(body)
    document_id = document["id"]
    document.pop("id")
    update_indexed_document(es, OFFER_INDEX, document, document_id)
    logger.info(f"Updated document: {document_id}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, choices=["add", "delete", "update"], required=True)
    parser.add_argument("--polling", type=int, default=1)
    args = parser.parse_args()
    if args.mode == "add":
        callback = add_callback
        queue = ADD_OFFER_QUEUE
    elif args.mode == "delete":
        callback = delete_callback
        queue = DELETE_OFFER_QUEUE
    elif args.mode == "update":
        callback = update_callback
        queue = UPDATE_OFFER_QUEUE
    else:
        raise ValueError("Invalid mode.")

    sleep(args.polling)  # wait for elasticsearch to start
    # elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")
    es_queue_on_index(es, queue, logger)

    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
