import sys

import json
import logging

import pika
from pika.exceptions import StreamLostError

logger = logging.getLogger("piccolo")
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


PICCOLO_RABBITMQ_URL = "amqp://guest:guest@127.0.0.1:5672/piccolo?heartbeat=0&connection_attempts=20"


def all_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


class Piccolo(object):
    exchange_name = 'piccolo'
    exchange_type = 'direct'

    listen_routing_key = None
    listen_queue_name = None

    publish_queue_name = None
    publish_routing_key = None

    queue_registry = dict()

    def __init__(self, amqp_url=PICCOLO_RABBITMQ_URL):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.
        :param str amqp_url: The AMQP url to connect with
        """
        self.connection = None
        self.channel = None
        self.closing = False
        self.consumer_tag = None
        self.url = amqp_url
        self._url = amqp_url
        self.publish_channel = None
        self.publish_init()
        self.initialize()

    def initialize(self):
        logger.info("create connect, %s" % PICCOLO_RABBITMQ_URL)
        connect = pika.BlockingConnection(
            pika.URLParameters(PICCOLO_RABBITMQ_URL))
        self.connection = connect
        logger.info("create channel")
        channel = self.connection.channel()
        self.channel = channel
        logger.info("create exchange")
        exchange = self.channel.exchange_declare(exchange=self.exchange_name,
                                                 durable=True)
        self.exchange = exchange
        logger.info("declare queue")
        queue = channel.queue_declare(self.publish_queue_name, durable=True)
        callback_queue = channel.queue_declare(self.listen_queue_name,
                                               durable=True)
        self.callback_queue = callback_queue
        self.queue = queue
        logger.info("bind routing")
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.publish_queue_name,
                                routing_key=self.publish_routing_key)

    def publish_init(self):
        logger.info("connection")
        connection = pika.BlockingConnection(
            pika.URLParameters(self._url))
        logger.info("channel")
        channel = connection.channel()
        logger.info("exchange")
        channel.exchange_declare(exchange=self.exchange_name,
                                 durable=True)
        logger.info("declare publish queue %s" % self.publish_queue_name)
        channel.queue_declare(self.publish_queue_name, durable=True)
        logger.info("bind routing")

        channel.queue_bind(exchange=self.exchange_name,
                           queue=self.publish_queue_name,
                           routing_key=self.publish_routing_key)
        self._publish_channel = channel

    def check_publish_message(self, payload):
        return payload

    def _publish(self, payload):
        self.check_publish_message(payload)
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        payload = payload.encode()
        if not self._publish_channel:
            self.publish_init()
        self._publish_channel.basic_publish(exchange=self.exchange_name,
                                            routing_key=self.publish_routing_key,
                                            body=payload)

    def publish(self, payload):
        try:
            self._publish(payload)
        except StreamLostError as e:
            logger.exception(e)
            self.publish_init()
            self._publish(payload)

    @classmethod
    def init_cls_registry(cls):
        subses = all_subclasses(cls)
        for sub_cls in subses:
            cls.queue_registry[sub_cls.publish_queue_name] = sub_cls

    def consume_payload(self, payload):
        pass

    def consumer_callback(self, ch, method, properties, body):
        logger.info("receive an message %s" % body)
        try:
            payload = json.loads(body.decode("utf-8"))
            res = self.consume_payload(payload=payload)
            return res
        except Exception as e:
            logger.exception(e)
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        channel = self.channel
        logger.info("listening %s" % self.listen_queue_name)
        channel.basic_consume(self.listen_queue_name,
                              self.consumer_callback)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        finally:
            self.connection.close()
            # supervisor reload
            exit(400)
