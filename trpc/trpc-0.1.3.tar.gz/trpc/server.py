import pika
import msgpack
from abc import ABC
from trpc import RemoteProcedureError

class Server(ABC):
	def __init__(self, queue, host='localhost'):
		self.__host = host
		self.__queue = queue
		self.__connection = pika.BlockingConnection(
				pika.ConnectionParameters(host=host))
		self.__channel = self.__connection.channel()
		self.__channel.queue_declare(queue=queue)
		self.__channel.basic_qos(prefetch_count=1)
		self.__channel.basic_consume(
				queue=queue,
				on_message_callback=self.__on_request
		)
	
	def __get_handler(self, name):
		try:
			return getattr(self, name)
		except AttributeError:
			message = 'This server does not implement "{}"'
			raise RemoteProcedureError(message.format(name))
	
	def __get_response(self, handler, content):
		try:
			response = handler(**content)
			return msgpack.packb(response, use_bin_type=True)
		except Exception as e:
			message = 'An unexpected error occurred (message={})'
			raise RemoteProcedureError(message.format(e))
	
	def __on_request(self, channel, method, props, body):
		pack = {
				'body': None,
				'error': False,
				'tag': method.delivery_tag,
				'reply_to': props.reply_to,
				'message': props.message_id,
				'correlation_id': props.correlation_id
		}
	
		try:
			content = msgpack.unpackb(body, raw=False)
			handler = self.__get_handler(props.message_id)
			response = self.__get_response(handler, content)	
			
			pack['body'] = response
			self.__send(**pack)
			
		except RemoteProcedureError as e:
			pack['body'] = str(e)
			pack['error'] = True
			self.__send(**pack)

	def __send(self, tag, body, message, reply_to, correlation_id, error):
		self.__channel.basic_publish(
				exchange='',
				body=body,
				routing_key=reply_to,
				properties=pika.BasicProperties(
					type=str(error),
					message_id=message,
					correlation_id=correlation_id
				)
		)

		self.__channel.basic_ack(delivery_tag=tag)

	def listen(self):
		#message = '[{}] Awaiting RPC requests'
		#print(message.format(self.__class__.__name__))
		self.__channel.start_consuming()

