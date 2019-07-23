from multiprocessing import cpu_count
from ..utils.config import update_flat_config_object


class Config:

    default_workers_cpu_based = cpu_count() + 1

    external_conf_file_section_name = 'muhomor'
    rpc_entry_point_attr = 'rpc_entry_point'
    rpc_methods_injected_attr = 'rpc_methods'
    rpc_caller_injected_attr = 'rpc'

    def __init__(self):
        self.amqp_uri: str = 'amqp://guest:guest@localhost:5672//'
        self.heartbeat: int = 11
        self.heartbeat_check: int = 2
        self.workers: int = 0  # set to 0 to use recommended settings, see  `default_workers_cpu_based` attr
        self.restart_dead_workers: bool = False
        self.amqp_prefix: str = 'muhomor'
        self.serializer: str = 'json'
        self.rpc_response_timeout: int = 30
        self.rpc_response_client_pool_timeout: float = 0.1
        self.rpc_reply_queue_ttl: int = 30000  # ms
        self.connect_timeout = 30
        self.transport_options = {
            'max_retries': 60,  # Max num of retries before we give up
            'interval_start': 1,  # How long we start sleeping between retries (sec)
            'interval_step': 1,  # By how much the interval is increased for each retry
            'interval_max': 5,  # Maximum number of seconds to sleep between retries
            'timeout': 5*60  # Maximum seconds waiting before we give up
        }
        self.amqp_ssl = False
        self.max_service_name_len = 30


class BrokerTemplate:

    def __init__(self, global_config: Config):
        self.PREFIX_RPC = f'{global_config.amqp_prefix}.rpc'
        self.PREFIX_RPC_REPLY = f'{global_config.amqp_prefix}.rpc.reply'
        self.PREFIX_EVENT = f'{global_config.amqp_prefix}.evt'

        self.EXCHANGE_NAME_RPC = self.PREFIX_RPC
        self.EXCHANGE_NAME_RPC_REPLY = self.PREFIX_RPC_REPLY
        self.EXCHANGE_NAME_PREFIX_EVENT = self.PREFIX_EVENT
        self.EXCHANGE_NAME_EVT = '{prefix}.{body}'.format(
            prefix=self.EXCHANGE_NAME_PREFIX_EVENT,
            body='{producer}')

        # exclusive: true, auto-delete: true
        self.QUEUE_TEMPLATE_BROADCAST_EVT = '{prefix}|{body}'.format(
            prefix=self.PREFIX_EVENT,
            body='{producer}:{event}(b)->{consumer}:{consumer_method}?{rand}')
        # durable: true
        self.QUEUE_TEMPLATE_SINGLETON_EVT = '{prefix}|{body}'.format(
            prefix=self.PREFIX_EVENT,
            body='{producer}:{event}(s)')
        # durable: true
        self.QUEUE_TEMPLATE_SERVICE_POOL_EVT = '{prefix}|{body}'.format(
            prefix=self.PREFIX_EVENT,
            body='{producer}:{event}(p)->{consumer}:{consumer_method}')
        self.QUEUE_TEMPLATE_RPC = '{prefix}|{body}'.format(
            prefix=self.PREFIX_RPC,
            body='{producer}')
        self.QUEUE_TEMPLATE_RPC_REPLY_PREFIX = f'{self.PREFIX_RPC}.reply'
        self.QUEUE_TEMPLATE_RPC_REPLY = '{prefix}|{body}'.format(
            prefix=self.QUEUE_TEMPLATE_RPC_REPLY_PREFIX,
            body='{producer}:{method}->{consumer}?{rand}')


config = Config()
broker_template = BrokerTemplate(config)


def get_config() -> Config:
    return config


def get_broker_template() -> BrokerTemplate:
    return broker_template


def configure(**kwargs):
    global broker_template
    update_flat_config_object(config, **kwargs)
    broker_template = BrokerTemplate(config)
