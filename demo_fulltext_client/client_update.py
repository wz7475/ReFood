import json
import sys

import pika
from config import UPDATE_OFFER_QUEUE

def generate_update_to_offer(param: int):
    return {
        "description": f"test{param} offer hdyż",
    }

if __name__ == '__main__':
    param = int(sys.argv[1])
    offer = generate_update_to_offer(param)

    # containerized - host='rabbitmq'
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='0.0.0.0', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=UPDATE_OFFER_QUEUE)
    channel.basic_publish(exchange='',
                          routing_key=UPDATE_OFFER_QUEUE,
                          body=json.dumps(offer))