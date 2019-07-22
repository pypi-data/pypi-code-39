import uuid
import pika
import msgpack
from trpc import RemoteProcedureError


class Client(object):
	def __init__(self, queue, host='localhost'):
		self.__host = host
		self.__queue = queue
		self.__response = None
		self.__correlation_id = None
		self.__connection = pika.BlockingConnection(
				pika.ConnectionParameters(host=host))
		self.__channel = self.__connection.channel()
		self.__result = self.__channel.queue_declare(
				'', exclusive=True)
		self.__callback_channel = self.__result.method.queue

		self.__channel.basic_consume(
				auto_ack=True,
				queue=self.__callback_channel,
				on_message_callback=self.__on_response
		)
	
	def __on_response(self, channel, method, props, body):
		if props.type == 'True':
			raise RemoteProcedureError(body.decode('utf-8'))

		if self.__correlation_id == props.correlation_id:
			self.__response = msgpack.unpackb(body, raw=False)

	def __getattr__(self, name):
		self.__response = None
		self.__correlation_id = str(uuid.uuid4)
		def request_procedure(**kwargs):
			self.__channel.basic_publish(
				exchange='',
				routing_key=self.__queue,
				body=msgpack.packb(kwargs),
				properties=pika.BasicProperties(
					message_id=name,
					reply_to=self.__callback_channel,
					correlation_id=self.__correlation_id
				)
			)

			while self.__response is None:
				self.__connection.process_data_events()
			return self.__response
		return request_procedure

