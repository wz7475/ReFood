import json
import pika


if __name__ == '__main__':
    offer = {
        "id": 1,
        "dish_id": 1,
        "seller_id": 1,
        "address_id": 1,
        "creation_date": "2021-01-01"
    }

    # rabbitmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='0.0.0.0', heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue='offer_queue')
    channel.basic_publish(exchange='',
                          routing_key='offer_queue',
                          body=json.dumps(offer))