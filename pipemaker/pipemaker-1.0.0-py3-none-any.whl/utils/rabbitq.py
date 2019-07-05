import pika

import logging
log = logging.getLogger()

class Rabbitq:
    """ base class for a rabbit queue """
    name = "default_queue"

    def __init__(self, persistent=False, heartbeat=0):
        """ connect to queue
        :param persistent: save queue and messages to disk
        :heartbeat: typically producer=0, consumer=180
        """
        self.persistent = persistent
        params = pika.ConnectionParameters(heartbeat=heartbeat)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.name, durable=self.persistent)

    def delete(self):
        """ clear the queue completely. usefult for testing """
        self.channel.stop_consuming()
        self.channel.queue_delete(queue=self.name)
        self.channel.close()

    ################################################################

    def put(self, body):
        """ put a message on the queue
        :body message to send
        """
        properties = dict()
        if self.persistent:
            properties["delivery_mode"]=2
        self.channel.basic_publish(exchange='', routing_key=self.name, body=body,
                               properties=pika.BasicProperties(**properties))

    #################################################################

    def listen(self):
        """ blocking listen. call onGet for each message received """
        self.channel.basic_consume(queue=self.name, on_message_callback=self.onGet)
        log.info(f"started listening {self.name}")
        try:
            self.channel.start_consuming()
        except:
            log.info(f"stopped listening {self.name}")

    def onGet(self, ch, method, properties, body):
        """ process received messages """
        body = body.decode()
        print(body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)