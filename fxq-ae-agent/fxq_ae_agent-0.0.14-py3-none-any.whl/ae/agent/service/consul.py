import http
import logging
import os
import socket

import requests
from fxq.core.stereotype import Service

from fxq.ae.agent.constants import ANALYTICS_SERVICE_ID

LOGGER = logging.getLogger(__name__)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

try:
    _host = os.environ["spring.cloud.consul.discovery.hostname"]
except KeyError:
    _host = host_name if 'fxquants.net' in host_name else host_ip
    LOGGER.warning(
        f'Environment Variable: "spring.cloud.consul.discovery.hostname" is not defined, falling back to {_host}')

try:
    _port = os.environ["spring.cloud.consul.discovery.port"]
except KeyError:
    _port = 5000
    LOGGER.warning(
        f'Environment Variable: "spring.cloud.consul.discovery.port" is not defined, falling back to {_port}')

try:
    _consul_host = os.environ["spring.cloud.consul.host"]
except KeyError:
    _consul_host = 'localhost'
    LOGGER.warning(f'Environment Variable: "spring.cloud.consul.host is not defined, falling back to {_consul_host}')

try:
    _consul_port = os.environ["spring.cloud.consul.port"]
except KeyError:
    _consul_port = 8500
    LOGGER.warning(f'Environment Variable: "spring.cloud.consul.port" is not defined, falling back to {_consul_port}')


@Service
class ConsulService:
    def __init__(self):
        self.host = _host
        self.port = _port
        self.consul_host = _consul_host
        self.consul_port = 8500
        self._register_host()

    def _register_host(self):
        service_def = {
            "ID": "service:ae-agent-5000",
            "Name": "ae-agent",
            "Tags": ["secure=false"],
            "Address": self.host,
            "Port": self.port,
            "Meta": {
            },
            "EnableTagOverride": False,
            "Check": {
                "DeregisterCriticalServiceAfter": "60s",
                "HTTP": f"http://{self.host}:{self.port}/api/actuator/health",
                "Interval": "10s"
            },
            "Weights": {
                "Passing": 10,
                "Warning": 1
            }
        }

        r = requests.put(f'http://{self.consul_host}:{self.consul_port}/v1/agent/service/register', json=service_def)
        if r.status_code != http.HTTPStatus.OK:
            raise Exception(f'Failed to register with Consul at http://{self.consul_host}:{self.consul_port}')

    def get_callback_host(self):
        r = requests.get(f'http://{self.consul_host}:{self.consul_port}/v1/agent/service/{ANALYTICS_SERVICE_ID}')
        if r.status_code != http.HTTPStatus.OK:
            raise Exception(
                f'Failed to get the Analytics Service using ID "analytics-8200", check it is registered with consul'
            )

        service_definition = r.json()

        return f'http://{service_definition["Address"]}:{service_definition["Port"]}'
