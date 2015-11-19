# -*- coding: utf-8 -*-

import logging
import time
import kombu
from kombu.mixins import ConsumerMixin
from google.protobuf.message import DecodeError
import stat_pb2
from gpio import Gpio


class Daemon(ConsumerMixin):
    def __init__(self, config):
        self.connection = None
        self.exchange = None
        self.queues = []
        self.config = config
        self._init_rabbitmq()
        self.gpio = Gpio(config)

    def _init_rabbitmq(self):
        """
        connect to rabbitmq and init the queues
        """
        self.connection = kombu.Connection(self.config.rabbitmq['broker-url'])
        exchange_name = self.config.rabbitmq['exchange-name']
        exchange = kombu.Exchange(exchange_name, type="direct")
        queue_name = self.config.rabbitmq['queue-name']
        logging.getLogger(__name__).info("listen following exchange: {exchange}, queue name: {queue}".
                                         format(exchange=exchange_name, queue=queue_name))
        queue = kombu.Queue(queue_name, exchange=exchange, durable=True)
        self.queues.append(queue)

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues, callbacks=[self.process_task])]

    def handle_data(self, data):
        if data.IsInitialized():
            self.gpio.manage_lights(data)
        else:
            logging.getLogger(__name__).warn("protobuff query not initialized")

    def process_task(self, body, message):
        logging.getLogger(__name__).debug("Message received")
        # Here, add the receipt of protobuf
        data_message = stat_pb2.StatRequest()
        try:
            data_message.ParseFromString(body)
            logging.getLogger(__name__).debug('query received: %s' % str(data_message))
        except DecodeError as e:
            logging.getLogger(__name__).warn("message is not a valid "
                                                        "protobuf task: {}".format(str(e)))
            message.ack()
            return
        try:
            self.handle_data(data_message)
            message.ack()
        except:
            logging.getLogger(__name__).warn("error while treating data.")
            message.requeue()
            time.sleep(10)

    def __del__(self):
        self.close()

    def close(self):
        if self.connection and self.connection.connected:
            self.connection.release()
        self.gpio.finalize()
