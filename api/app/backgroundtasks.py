from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from .models import Outbox
from .sqlalchemy import engine
from .logger import get_logger


def send_message(rabbitmq_channel, payload: str, routing_key: str):
    """
    Sends a message to the RabbitMQ broker.
    :param payload: message payload
    :param routing_key: routing key
    """
    rabbitmq_channel.basic_publish(exchange="", routing_key=routing_key, body=payload)

def send_messages_from_outbox(rabbitmq_channel, logger=get_logger()):
    """
    Sends all messages from the outbox.
    :param rabbitmq_channel: RabbitMQ channel
    :param logger: logger
    """
    with Session(engine) as session:
        with session.begin():
            outbox_entries = session.query(Outbox).filter(Outbox.status != 'sent').all()
            for entry in outbox_entries:
                try:
                    send_message(rabbitmq_channel, entry.payload, entry.routing_key)
                    entry.status = "sent"
                except Exception as e:
                    logger.error(f"Error while sending message: {e}")
    logger.info("Outbox processed successfully.")