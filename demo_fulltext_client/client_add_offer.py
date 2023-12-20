import json
import sys

import pika
from config_copy import ADD_OFFER_QUEUE

def generate_offer(param: int):
    return {
        "id": param,
        "dish_id": param,
        "seller_id": param,
        "address_id": param,
        "creation_date": "2021-01-01",
        "description": f"test{param} offer hdyż",
    }

if __name__ == '__main__':
    param = int(sys.argv[1])
    offer = generate_offer(param)

    # containerized - host='rabbitmq'
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='0.0.0.0', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=ADD_OFFER_QUEUE)
    channel.basic_publish(exchange='',
                          routing_key=ADD_OFFER_QUEUE,
                          body=json.dumps(offer))