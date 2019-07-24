# -*- coding: utf-8 -*-

import importlib
import json
import os
import sys
import urllib.parse

try:
    import requests

    class ArchitectSession(requests.Session):
        def __init__(self, base_url):
            self.base_url
            super()

        def request(self, method, url, *args, **kwargs):
            url = urllib.parse.urljoin(self.base_url, url)
            return super().request(method, url, *args, **kwargs)
except ImportError:
    requests = None

try:
    import grpc
except ImportError:
    grpc = None


sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'architect_services'))


services = {}
datastores = {}


class ArchitectService:
    def __init__(self, service_name, config):
        self.config = config
        if config['interface'] == 'rest':
            if requests is None:
                raise Exception('Include requests in your requirements.txt')
            self.client = ArchitectSession('{}:{}'.format(self.config.host, self.config.port))
        elif config['interface'] == 'grpc':
            if grpc is None:
                raise Exception('Include grpcio in your requirements.txt')
            service_folder = service_name.replace('-', '_')
            self.grpc_pb = importlib.import_module('architect_services.{}.service_pb2_grpc'.format(service_folder))
            self.defs = importlib.import_module('architect_services.{}.service_pb2'.format(service_folder))
            channel = grpc.insecure_channel('{}:{}'.format(config['host'], config['port']))
            self.client = self.grpc_pb.ArchitectStub(channel)


def service(service_name):
    service = services.get(service_name)
    if service is None:
        key = 'ARC_{}'.format(service_name.replace('/', '_').replace('-', '_').upper())
        try:
            value = os.environ[key]
        except:
            raise Exception('{} is required but has not been started'.format(service_name))
        config = json.loads(value)
        services[service_name] = service = ArchitectService(service_name, config)

    return service


def datastore(datastore_name):
    datastore = datastores.get(datastore_name)
    if datastore is None:
        key = 'ARC_DS_{}'.format(datastore_name.replace('-', '_').upper())
        try:
            value = os.environ[key]
        except:
            raise Exception('{} is required but has not been started'.format(datastore_name))
        datastores[datastore_name] = datastore = json.loads(value)
    return datastore


def current_service():
    current_service = service(os.environ['ARC_CURRENT_SERVICE'])
    if current_service.grpc_pb:
        current_service.Servicer = current_service.grpc_pb.ArchitectServicer
        current_service.add_servicer = current_service.grpc_pb.add_ArchitectServicer_to_server
    return current_service
