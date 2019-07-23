from .config import get_config, get_broker_template
from kombu import Connection, Queue, Exchange, Consumer, Producer
from typing import Dict, Any, Union
import socket
from kombu.message import Message
from ..exceptions import RpcMethodCallTimeout, PublishingError
from logging import getLogger

logger = getLogger(__name__)

rpc_exchange: Exchange = None
evt_exchange: Dict[str, Exchange] = {}


def get_rpc_exchange() -> Exchange:
    global rpc_exchange
    if rpc_exchange is None:
        rpc_exchange = Exchange(get_broker_template().EXCHANGE_NAME_RPC,
                                type='topic',
                                durable=True,
                                delivery_mode=Exchange.PERSISTENT_DELIVERY_MODE,
                                auto_delete=False)
    return rpc_exchange


def get_evt_exchange(service_name: str) -> Exchange:
    global evt_exchange
    if service_name not in evt_exchange:
        evt_exchange[service_name] = Exchange(get_broker_template().EXCHANGE_NAME_EVT.format(producer=service_name),
                                              type='topic',
                                              durable=True,
                                              delivery_mode=Exchange.PERSISTENT_DELIVERY_MODE,
                                              auto_delete=True)
    return evt_exchange[service_name]


def make_connection(heartbeats_on: bool = True) -> Connection:
    config = get_config()
    logger.debug(f'Making connection in make_connection, config: {config.amqp_uri}')
    logger.debug(f'Making connection in make_connection, config func: {get_config().amqp_uri}')
    c = Connection(config.amqp_uri,
                      heartbeat=config.heartbeat if heartbeats_on else 0,
                      connect_timeout=config.connect_timeout,
                      transport_options=config.transport_options)
    logger.debug(f'Created  connection: {c}')
    return c


def publish_rpc_call(service_name: str, method_name: str,
                     args: Union[Dict[str, Any], None],
                     producer: Producer,
                     consumer: Consumer,
                     reply_queue: Queue,
                     correlation_id: str):
    config = get_config()
    try:
        consumer.add_queue(reply_queue)
        consumer.consume(no_ack=True)
        producer.publish(args,
                         exchange=get_rpc_exchange(),
                         routing_key=f'{service_name}.{method_name}',
                         # declare=[reply_queue],
                         reply_to=reply_queue.name,
                         correlation_id=correlation_id)
        consumer.connection.drain_events(timeout=config.rpc_response_timeout)
        consumer.cancel()
        consumer.queues = {}
    except socket.timeout as e:
        raise RpcMethodCallTimeout
    except BaseException as e:
        logger.warning(f'Rpc call publishing failed: {e}')
        raise PublishingError


def rpc_queue(name: str, exchange: Exchange, routing_key: str) -> Queue:
    return Queue(
        name,
        exchange=exchange,
        routing_key=routing_key,
        durable=True,
        message_ttl=30,
        # expires=5000,
        auto_delete=False
    )


def evt_queue(name: str, exchange: Exchange, routing_key: str, binding_arguments: Dict[str, Any] = None) -> Queue:
    return Queue(
        name,
        exchange=exchange,
        routing_key=routing_key,
        durable=True,
        message_ttl=10,
        # expires=5000,
        auto_delete=False,
        binding_arguments=binding_arguments
    )


def is_rpc_exchange(exchange_name: str) -> bool:
    return exchange_name == get_broker_template().EXCHANGE_NAME_RPC


def is_rpc_reply_message(message: Message, for_service: str) -> bool:
    rk = message.delivery_info['routing_key']
    if message.delivery_info['exchange'] == '' and rk.startswith(get_broker_template().QUEUE_TEMPLATE_RPC_REPLY_PREFIX):
        return rk.split('->')[-1].startswith(f'{for_service}?')
    return False


def is_events_exchange(exchange_name: str) -> bool:
    return exchange_name.startswith(get_broker_template().EXCHANGE_NAME_PREFIX_EVENT)


def message_requires_reply(message: Message) -> bool:
    return message and hasattr(message, 'properties') and \
           'reply_to' in message.properties and \
           'correlation_id' in message.properties
