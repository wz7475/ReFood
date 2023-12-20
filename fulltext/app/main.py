import json
import pika
from elasticsearch import Elasticsearch
from logger import get_logger

logger = get_logger()


def callback(ch, method, properties, body):
    offer = json.loads(body)
    es.index(index="offers", id=offer["id"], body=offer)
    logger.info(f"Received offer: {offer['id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    # elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")

    logger.info(f"{es.info()}")

    if not es.indices.exists(index="offers"):
        es.indices.create(index='offers', ignore=400)
        logger.info(f"Index 'offers' created.")
    else:
        logger.info(f"Index 'offers' already exists.")
    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue='offer_queue')
    channel.basic_consume(queue='offer_queue', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
