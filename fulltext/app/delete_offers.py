import json
import pika
from elasticsearch import Elasticsearch
from logger import get_logger
from es_tools import create_index, delete_indexed_document
from config import OFFER_INDEX, DELETE_OFFER_QUEUE

logger = get_logger()


def callback(ch, method, properties, body):
    offer = json.loads(body)
    offer_id = offer["id"]
    delete_indexed_document(es, OFFER_INDEX, offer_id)
    logger.info(f"Deleted offer: {offer['id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    # elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")
    create_index(es, OFFER_INDEX, logger)

    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=DELETE_OFFER_QUEUE)
    channel.basic_consume(queue=DELETE_OFFER_QUEUE, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
