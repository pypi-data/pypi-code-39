from multiprocessing import Value
from kombu import Queue, uuid, Consumer, Producer
import sys
import queue
from typing import Dict, Any, Union, List
import threading
import os
import time
import socket
from .config import Config, BrokerTemplate, get_config, get_broker_template
from .transport import (
    rpc_queue,
    evt_queue,
    is_rpc_exchange,
    is_rpc_reply_message, is_events_exchange,
    message_requires_reply
)
from ..utils.serialization import serialize_exception, serialize_safe as safe_exc_serialize, deserialize_exception
from ..exceptions import (
    UnserializableValueError, IncorrectSignature, RpcMethodNotFound, InternalError, AccessDenied, RemoteError
)
import inspect
from functools import partial
import types
from .transport import get_rpc_exchange, get_evt_exchange, make_connection, publish_rpc_call
from .entry_points import RpcEntryPoint, _is_entrypoint, get_entrypoint
from kombu.utils.debug import setup_logging
from logging import getLogger

logger = getLogger(__name__)

# setup_logging(loglevel=logging.DEBUG, loggers=['kombu.connection', 'kombu.channel'])


W_CONN_LOST = 'Connection to broker lost, trying to re-establish connection...'


class RpcReply:
    def __init__(self, result=None, exception=None, correlation_id=None):
        self.result: Any = result
        self.exception: Any = exception
        self.correlation_id: Union[None, str] = correlation_id
        self._json_response = {'result': None, 'error': None}

    @property
    def json_response(self):
        if self.result is not None:
            try:
                # self._json_response['result'] = kombu_serialization.dumps(self.result, config.serializer)[-1]
                self._json_response['result'] = self.result
            except Exception:
                self.exception = UnserializableValueError(self.result)
                self._json_response['result'] = None
        if self.exception is not None:
            f = serialize_exception if isinstance(self.exception, BaseException) else safe_exc_serialize
            self._json_response['error'] = f(self.exception)
        return self._json_response


class WorkerBase:

    def __init__(self, name: str, heartbeats_on: bool = True):
        self.name = name
        self.worker_id = os.getpid()
        self.worker_alias = WorkerBase.alias(self.name, self.worker_id)
        self.config: Config = get_config()
        self.broker_template: BrokerTemplate = get_broker_template()
        logger.debug(f'Making connection in WorkerBase, config: {self.config.amqp_uri}')
        self.connection = make_connection(heartbeats_on)
        self.rpc_exchange = get_rpc_exchange()
        self.incoming_message_log_on = False
        self.producer = Producer(self.connection, serializer=self.config.serializer)
        self._correlation_id = None

    @staticmethod
    def alias(service_name, worker_id):
        return f'Worker::{service_name}<{worker_id}>'

    @property
    def next_correlation_id(self):
        self._correlation_id = uuid()
        return self._correlation_id

    @property
    def callbacks(self):
        callbacks = list()
        if self.incoming_message_log_on:
            callbacks.append(self.log_incoming_message)
        callbacks.append(self.on_message)
        return callbacks

    def on_message(self, body, message):
        raise NotImplementedError('Subclass must implement this functionality')

    def log_incoming_message(self, body, message):
        if is_rpc_exchange(message.delivery_info["exchange"]):
            logger.debug(f'RpcRequest {message.delivery_info["exchange"]}:{message.delivery_info["routing_key"]}')
        elif is_rpc_reply_message(message, self.name):
            logger.debug(f'RpcReply {message.delivery_info}')
        elif is_events_exchange(message.delivery_info["exchange"]):
            logger.debug(f'Event {message.delivery_info["exchange"]}:{message.delivery_info["routing_key"]}')

    def should_stop(self) -> bool:
        raise NotImplementedError('Subclass must implement this functionality')

    def stop(self):
        logger.debug(f'Worker is stopping...')
        try:
            self.connection.release()
        except BaseException as e:
            logger.warn(f'Error releasing connection: {e}')
        logger.info(f'Worker stopped.')

    def heartbeat(self, frequency: int = 1):
        while not self.should_stop():
            try:
                self.connection.heartbeat_check()
            except BaseException as e:
                logger.warning(f'Heartbeat failed: {e}')
                pass
            time.sleep(frequency)
        logger.info(f'Heartbeats stopped.')

    def start_heartbeats(self):
        if not self.should_stop():
            threading.Thread(target=self.heartbeat, args=(self.config.heartbeat_check,), daemon=True).start()


class RpcWorker(WorkerBase):

    def __init__(self, name: str, heartbeats_on: bool = True):
        WorkerBase.__init__(self, name, heartbeats_on=heartbeats_on)
        self._heartbeat_sig = queue.Queue()
        self._process_stop = None
        self._stopping = False
        self._consuming_channel = None
        self._producing_channel = None
        self.queues = list()

    def set_process_stopper(self, val: Union[Value, None]):
        self._process_stop = val

    def should_stop(self) -> bool:
        return self._stopping or not (self._process_stop is None or self._process_stop.value == 0)

    def on_message(self, body, message):
        raise NotImplementedError('Subclass must implement this functionality')


class RpcCallPublisher(WorkerBase):

    def _setup_publisher(self):
        self.rpc_response_client_pool = queue.Queue()
        self.queues_for_rpc_reply = dict()
        logger.debug(f'Connection in _setup_publisher: {self.connection}')
        self.consumer_rpc_reply = Consumer(self.connection,
                                           callbacks=self.callbacks,
                                           no_ack=False,
                                           auto_declare=True,
                                           accept={'application/json'},
                                           prefetch_count=1)

    def setup_publisher(self):
        self._setup_publisher()

    def _make_queue_for_rpc_reply(self, service: str, method: str) -> Queue:
        reply_queue = Queue(self.broker_template.QUEUE_TEMPLATE_RPC_REPLY.
                            format(producer=service, method=method, consumer=self.name, rand=uuid()),
                            exchange=self.rpc_exchange,
                            exclusive=True,
                            auto_delete=True,
                            no_ack=True,
                            queue_arguments={'x-expires': self.config.rpc_reply_queue_ttl})
        if service not in self.queues_for_rpc_reply:
            self.queues_for_rpc_reply[service] = {}
        self.queues_for_rpc_reply[service][method] = reply_queue
        return reply_queue

    def get_queue_for_rpc_reply(self, service: str, method: str) -> Queue:
        if service in self.queues_for_rpc_reply and method in self.queues_for_rpc_reply[service]:
            return self.queues_for_rpc_reply[service][method]
        return self._make_queue_for_rpc_reply(service, method)

    def should_stop(self) -> bool:
        pass

    def _get_from_rpc_response_client_pool(self):
        return self.rpc_response_client_pool.get(block=True,
                                                 timeout=self.config.rpc_response_client_pool_timeout)

    def rpc(self, service_name, method_name, args: Dict[str, Any] = None):
        publish_rpc_call(service_name, method_name, args,
                         producer=self.producer, consumer=self.consumer_rpc_reply,
                         reply_queue=self.get_queue_for_rpc_reply(service_name, method_name),
                         correlation_id=self.next_correlation_id)
        response = None
        try:
            response = self._get_from_rpc_response_client_pool()
        except queue.Empty:
            pass
        if response and 'error' in response and response['error'] is not None:
            e = deserialize_exception(response['error'], RemoteError)
            if isinstance(e, AccessDenied):
                logger.warning(f'RPC access denied to {service_name}.{method_name}')
            raise e
        return response['result'] if response and 'result' in response else None

    def verify_correlation_id(self, message) -> bool:
        return message and hasattr(message, 'properties') and \
               'correlation_id' in message.properties and \
               message.properties['correlation_id'] == self._correlation_id

    def is_my_rpc_reply_message(self, message) -> bool:
        return is_rpc_reply_message(message, self.name) and self.verify_correlation_id(message)

    def on_message(self, body, message):
        if self.is_my_rpc_reply_message(message):
            self._on_if_my_rpc_reply(body, message)
        message.ack()

    def on_rpc_reply(self, body, message):
        if self.is_my_rpc_reply_message(message):
            self._on_if_my_rpc_reply(body, message)

    def _on_if_my_rpc_reply(self, body, message):
        self.rpc_response_client_pool.put(body)


class RpcClient(RpcWorker, RpcCallPublisher):

    def __init__(self, name: str):
        RpcWorker.__init__(self, name, heartbeats_on=False)
        logger.debug(f'MUHOMOR CONFIG IN RpcClient: {get_config().amqp_uri}')
        logger.debug(f'MUHOMOR CONFIG IN RpcClient PARENT: {self.config.amqp_uri}')
        self.setup_publisher()

    def on_message(self, body, message):
        RpcCallPublisher.on_message(self, body, message)


# TO-DO: test launching when there are still messages in queues
class RpcServer(RpcWorker, RpcCallPublisher):

    def __init__(self, name: str):
        RpcWorker.__init__(self, name, heartbeats_on=True)
        # RpcCallPublisher.__init__(self, name)
        self.rpc_result_server_pool = queue.Queue()
        self.rpc_method_providers = {}
        self.event_handlers = {}
        self.evt_exchange = get_evt_exchange(self.name)
        self.rpc_routing_key = f'{self.name}.*'
        self.evt_routing_key = '*.*'
        self.provider = None

        self._consuming_channel = None
        self._producing_channel = None
        self._pending_rpc_call_message = None

        self.rpc_queue = rpc_queue(self.broker_template.QUEUE_TEMPLATE_RPC.format(producer=self.name),
                                   self.rpc_exchange, self.rpc_routing_key)

        # self.evt_queue = evt_queue(f'evt.{self.name}', self.evt_exchange, self.evt_routing_key,
        #                            binding_arguments={
        #                                'event': 'ping',
        #                                'x-match': 'any'
        #                            })

        self.queues.append(self.rpc_queue)

        self.consumer: Consumer = None

        self.setup()
        self.setup_publisher()

        # self.start_heartbeats()
        logger.info(f'Created worker with URI `{self.connection.as_uri()}`')

        self.rpc_threads = dict()

    def setup(self):
        self.consumer = Consumer(self.connection,
                                 queues=self.queues,
                                 callbacks=self.callbacks,
                                 no_ack=False,
                                 auto_declare=True,
                                 accept={'application/json'},
                                 prefetch_count=1)
        self.consumer.consume()

    def _enter_rpc_entry_point(self, entry_point: RpcEntryPoint, params: Union[Dict[str, Any], List[Any]],
                               correlation_id: str = None, return_result: bool = False) -> Union[RpcReply, None]:
        """
        Call wrapped RPC method, locally.
        :param entry_point: RpcEntryPoint instance created using decorator.
        :param params: Called Rpc method parameters.
        :param correlation_id: If answer is not required, it should be set to None.
        :param return_result: If set to True, result will be returned directly to caller.
                              Otherwise it will be saved in results queue.
        :return:
        """
        reply = RpcReply(correlation_id=correlation_id)
        try:
            reply.result = entry_point.call(params)
        except BaseException as e:
            reply.exception = e
        if return_result:
            return reply
        if correlation_id is not None:
            self.rpc_result_server_pool.put(reply)
        else:
            del reply
        return

    def _set_pending_rpc_call_message(self, message, body):
        message.properties['rpc_result_correlation_id'] = uuid()
        message.properties['queued_at'] = time.time()
        message.properties['body'] = body
        # logger.debug('Setting pending rpc message')
        self._pending_rpc_call_message = message
        return message.properties['rpc_result_correlation_id']

    def _publish_rpc_reply(self, message, reply: RpcReply):
        self._pending_rpc_call_message = None
        try:
            if message_requires_reply(message):
                logger.debug(f'Publishing reply '
                             f'{reply.json_response}')
                self.producer.publish(
                    reply.json_response,
                    exchange='',
                    routing_key=message.properties['reply_to'],
                    correlation_id=message.properties['correlation_id'],
                    serializer=self.config.serializer,
                    retry=True)
        except Exception as e:
            logger.warning(f'Publishing RPC reply failed: {e}', e)

    def _get_rpc_reply(self):
        res = None
        try:
            res = self.rpc_result_server_pool.get_nowait()
        except queue.Empty:
            pass
        except Exception as e:
            logger.warning(f'Getting rpc call result queue error: {e}')
        return res

    def setup_provider(self, provider):
        try:
            self.provider = provider()
            setattr(self.provider, self.config.rpc_methods_injected_attr, dict())
            setattr(self.provider, self.config.rpc_caller_injected_attr, self.rpc)
        except BaseException:
            logger.exception(f'Instantiation of provider in {self.worker_alias} failed.')
            raise
        for method_name, method in inspect.getmembers(provider, _is_entrypoint):
            entrypoint = get_entrypoint(method)
            try:
                entrypoint.bind(self.provider, method_name)
            except BaseException:
                logger.exception(f'Binding RPC provider for {self.worker_alias} failed.')
                raise
        logger.debug(f'PRC provider for {self.worker_alias} is set.')

    def connect(self):
        # revived_connection = self.connection.clone()
        logger.debug(f'Worker {self.worker_id} is connecting')
        try:
            self.connection.ensure_connection(max_retries=3)
            self._consuming_channel = self.connection.default_channel
            self._producing_channel = self.connection.channel()

            self.consumer_rpc_reply.revive(self._consuming_channel)
            self.producer.revive(self._producing_channel)
            self.consumer.revive(self._consuming_channel)
            self.consumer.consume()
        except BaseException:
            logger.exception('Connection failed')

    # TO-DO: implement real services auth functionality
    def validate_rpc_access(self, calling_service: str, method: str) -> Union[bool, BaseException]:
        if calling_service == 'subscriptions':
            if method == 'mint':
                return AccessDenied(f'Service `{calling_service}` has no access to method `{self.name}.{method}`')
        return True

    def on_message(self, body, message):
        if is_rpc_exchange(message.delivery_info["exchange"]):
            self.on_rpc(body, message)
        elif is_rpc_reply_message(message, self.name):
            self.on_rpc_reply(body, message)
        elif is_events_exchange(message.delivery_info["exchange"]):
            self.on_event(body, message)

    def on_rpc(self, body, message):
        provider = self.get_provider_for_method(message.delivery_info['routing_key'])
        corr_id = None

        requesting_service = 'subscriptions'

        valid_access = self.validate_rpc_access(requesting_service, provider.method_name)
        if isinstance(valid_access, BaseException):
            if message_requires_reply(message):
                # corr_id = self._set_pending_rpc_call_message(message)
                logger.error(f'Attempt of illegal access of method {provider.method_name} '
                             f'from service {requesting_service}')
                self._publish_rpc_reply(message, RpcReply(exception=valid_access, correlation_id=uuid()))
        else:
            if message_requires_reply(message):
                # logger.debug('RPC message requires reply... Putting in pending queue...')
                corr_id = self._set_pending_rpc_call_message(message, body)

            t_name = f'EP({provider.method_name}):{len(self.rpc_threads) + 1}'
            t = threading.Thread(target=self._enter_rpc_entry_point,
                                 daemon=True,
                                 name=t_name,
                                 args=(provider, body,),
                                 kwargs={'correlation_id': corr_id})
            # self.rpc_threads[t_name] = t
            t.start()
        message.ack()
        # logger.debug(f'RPC message in pending queue 2222: {self._pending_rpc_call_message}, corrid={corr_id}')

    def on_event(self, body, message):
        producer_name = message.delivery_info["exchange"].split(".")[-1]
        routing_key = message.delivery_info['routing_key']
        try:
            evt_handler_provider = self.get_event_handler(producer_name, routing_key)
            if evt_handler_provider is not None:
                logger.debug(f'Event handler provider: {evt_handler_provider} {message.payload}.')
                if evt_handler_provider:
                    evt_handler_provider.call(**body)
        except BaseException:
            logger.exception('Event handling failed.')
        message.ack()

    def dispatch(self, event_name: str, payload: Any = None, event_sender: str = None):
        self.producer.publish(payload, exchange=self.evt_exchange,
                              routing_key=f'{event_sender or self.name}.{event_name}')

    def check_pending_rpc_call_message(self):
        if self._pending_rpc_call_message is not None:
            queued_at = self._pending_rpc_call_message.properties['queued_at'] or 0
            if time.time() - queued_at >= self.config.rpc_response_timeout:
                logger.warning(f'Pending rpc call message {self._pending_rpc_call_message} expired...')
                self._pending_rpc_call_message = None
            else:
                res: RpcReply = self._get_rpc_reply()
                if res is not None and res.correlation_id and \
                        self._pending_rpc_call_message.properties['rpc_result_correlation_id'] == res.correlation_id:
                    self._publish_rpc_reply(self._pending_rpc_call_message, res)

    @property
    def consume_paused(self):
        return self._pending_rpc_call_message is not None

    def on_consuming_iteration(self):
        pass

    # TO-DO: re-connect in case of failure in heartbeats thread
    def consume(self, timeout=None, safety_interval=1, **kwargs):
        if not self._stopping:
            elapsed = 0
            self.connect()
            while not self.should_stop():
                self.on_consuming_iteration()
                self.check_pending_rpc_call_message()
                if not self.consume_paused:
                    try:
                        self.connection.drain_events(timeout=safety_interval)
                    except socket.timeout as e:
                        elapsed += safety_interval
                        self.connection.heartbeat_check()
                        if timeout and elapsed >= timeout:
                            logger.debug(f'Socket timeout in consuming loop: {e}')
                            # raise ConsumingTimeout(e.__str__())
                            raise
                    except socket.error as e:
                        logger.warning(f'Socket error in consuming loop: {e}')
                        if not self.should_stop():
                            raise
                    else:
                        elapsed = 0

    def run(self, **kwargs):
        while not self.should_stop():
            try:
                # pass
                self.consume(**kwargs)
            except (self.connection.connection_errors + self.connection.channel_errors):
                logger.warning(W_CONN_LOST)
                # logger.warning(W_CONN_LOST, exc_info=1)
            except KeyboardInterrupt:
                self._stopping = True
                break
        self.stop()

    def get_provider_for_method(self, routing_key: str) -> RpcEntryPoint:
        method_name = routing_key.split(".")[-1]
        try:
            rpc_methods = getattr(self.provider, self.config.rpc_methods_injected_attr)
        except BaseException as e:
            logger.error(f'No {self.config.rpc_methods_injected_attr} in provider...')
            raise RpcMethodNotFound(f'Method {method_name} not found')

        if method_name in rpc_methods:
            if not hasattr(rpc_methods[method_name], 'call'):
                raise InternalError(f'Provider of method {method_name} is not callable')
            return rpc_methods[method_name]
        else:
            raise RpcMethodNotFound(f'Method {method_name} not found')

    # def get_event_handler(self, service_name, routing_key):
    #     event_name = routing_key
    #     if evt_handlers and self.name in evt_handlers and service_name in evt_handlers[self.name] and \
    #             event_name in evt_handlers[self.name][service_name]:
    #         if hasattr(evt_handlers[self.name][service_name][event_name], 'call'):
    #             return evt_handlers[self.name][service_name][event_name]
    #         else:
    #             logger.warning(f'Event handler provider of service `{self.name}` '
    #                            f'for event {service_name}.{event_name} is not callable')
    #     return None

# class RpcService:
#
#     def __init__(self, service_caller: Callable, resource: object, connection_releaser: Callable):
#         self.service_caller = service_caller
#         self.resource = resource
#         self.connection_releaser = connection_releaser
#
#     def enable_exclusive_connection(self, value: bool = True):
#         self.resource.exclusive_request_rpc_connection = value
#         if not value:
#             self.connection_releaser()
#
#     def __getattr__(self, name):
#         return self.service_caller(name)
