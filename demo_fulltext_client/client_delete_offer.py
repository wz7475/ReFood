import json
import sys

import pika
from config import DELETE_OFFER_QUEUE


def generate_offer_to_rm(param: int):
    return {
        "id": param
    }


if __name__ == '__main__':
    param = int(sys.argv[1])
    offer = generate_offer_to_rm(param)

    # containerized - host='rabbitmq'
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='0.0.0.0', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=DELETE_OFFER_QUEUE)
    channel.basic_publish(exchange='',
                          routing_key=DELETE_OFFER_QUEUE,
                          body=json.dumps(offer))
