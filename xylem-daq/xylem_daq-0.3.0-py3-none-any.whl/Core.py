'''
Master component which is aware of all components in the system and
interfaces with the human operator.

'''
from __future__ import absolute_import
from __future__ import print_function

import zmq
import time
import struct
import threading
from collections import defaultdict
import logging
from . import protocol
from .common import MSEC_TO_SEC

class Core(object):

    def __init__(self, router_address, log_address):
        self.context = zmq.Context()
        self.router = self.context.socket(zmq.ROUTER)
        self.router.bind(router_address)
        self.logger = self.context.socket(zmq.PUB)
        self.logger.connect(log_address)
        time.sleep(0.1)  # ZeroMQ slow joiner syndrome fix
        self.log('INFO', 'Started up')
        self.poller = zmq.Poller()
        self.poller.register(self.router, zmq.POLLIN)
        self.clients = []
        self.min_heartbeat_ms = 999999
        self.address_service = {}
        self.addresses_cache = {}
        self.state = ''
        self.isStateAllowed = lambda x: True
        self.controller_handlers = {
                '*': print,
                'PRINT': print,
                'CLIENTS': self.clients_handler,
                'STATE': self.state_update_handler,
                'STATE REQUEST': self.state_request_handler,
                'ACTION': self.action_handler,
                'ACTIONS': self.action_list_handler,
                }
        self.action_count = 0
        self.pending_actions = {}
        self._event_handlers = {
                'new_component': [],
                'lost_component': [],
                'state_change': [],
                'action_request': [],
                'action_complete': [],
                }

    def addHandler(self, handler):
        '''
        Add the given event handler.

        '''
        event = handler.event
        self._event_handlers[event].append(handler)

    def log(self, level, message):
        '''
        Send the given message to the global log.

        '''
        timestamp = time.time()
        component = 'Core'
        m = protocol.log_create(level, timestamp, component, message)
        self.logger.send_multipart(m)
        return

    def run(self):
        while True:
            to_remove = []
            for client in self.clients:
                if time.time() > client.expiry:
                    to_remove.append(client)
                    print('Lost client named %s' % client.name)
                    self.log('INFO', 'Lost client "%s"' % client.name)
            actions_to_remove = []
            for client in to_remove:
                self.clients.remove(client)
                for handler in self._event_handlers['lost_component']:
                    handler.handle(client.name, self.client_list())
                for action_id_core, data in self.pending_actions.items():
                    client_id = data['_client_id']
                    controller_id = data['_controller_id']
                    if client_id == client.client_id:
                        header = 'ACTION RESULT'
                        payload = {
                                'id': action_id_core,
                                'result': 'ERROR: component died',
                        }
                        response = protocol.controller_create(header, payload)
                        self.router.send_multipart([controller_id] + response)
                        actions_to_remove.append(action_id_core)
            for action_id in actions_to_remove:
                del self.pending_actions[action_id]
            sockets = dict(self.poller.poll(self.min_heartbeat_ms))
            if self.router in sockets:
                message = self.router.recv_multipart()
                try:
                    self.handle(message)
                except Exception as e:
                    logging.exception(e)

    def client_list(self):
        '''
        Return a list of client names.

        '''
        clients = [client.name for client in self.clients]
        return clients

    def get_client(self, client_id):
        '''
        Return the Client object with the given id, or None if there is
        no such client.

        '''
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def get_client_id(self, name):
        '''
        Return the client id of the given name.

        '''
        for client in self.clients:
            if client.name == name:
                return client.client_id
        return None

    def client_actions(self):
        '''
        Return a dict mapping client name to {action name =>
        description}.

        '''
        actions = {client.name: client.actions for client in
                self.clients}
        return actions

    def send_state_update(self, new_state, client_id=None):
        '''
        Send a state update message to the specified client, or to
        all of them if client_id is ``None``.

        '''
        old_state = self.state
        self.state = new_state
        message = protocol.state_update_create(new_state)
        if client_id:
            self.router.send_multipart([client_id] + message)
        else:
            for client in self.clients:
                self.router.send_multipart([client.client_id] + message)

    def send_action(self, client_name, action_name, params,
            controller_id):
        '''
        Send an action message to the specified client.

        '''
        for handler in self._event_handlers['action_request']:
            handler.handle(client_name, action_name, params)
        client_id = self.get_client_id(client_name)
        if client_id is None:
            return None
        action_id = self.action_count
        self.action_count += 1
        action_id_core = self.action_count
        self.pending_actions[action_id_core] = {
                '_controller_id': controller_id,
                '_client_id': client_id,
                'client_name': client_name,
                'action_name': action_name,
                'params': params,
                'id': action_id_core,
        }
        action_message = protocol.action_create(action_id_core, action_name, params)
        self.router.send_multipart([client_id] + action_message)
        return action_id_core

    def clients_handler(self, message):
        header = 'CLIENTS'
        payload = {
                'result': self.client_list(),
        }
        response = {
                'header': header,
                'message': payload,
        }
        print(response)
        return response

    def state_request_handler(self, message):
        return {
                'header': 'STATE REQUEST',
                'message': {
                    'result': self.state,
                }
        }

    def state_update_handler(self, message):
        new_state = message['message']
        if self.isStateAllowed(new_state):
            self.send_state_update(new_state)
            header = 'STATE'
            payload = {'result': 'UPDATED'}
        else:
            header = 'STATE'
            payload = {
                    'result': 'NOT UPDATED',
                    'metadata': {'reason': 'STATE NOT ALLOWED'},
            }
        response = {
                'header': header,
                'message': payload,
        }
        return response

    def action_handler(self, message):
        self.log('DEBUG', 'received action: %s' % message)
        payload = message['message']
        action_name = payload['action_name']
        client_name = payload['client_name']
        params = payload['params']
        controller_id = message['_controller_id']
        action_id_core = self.send_action(client_name, action_name,
                params, controller_id)
        metadata = {
            'client_name': client_name,
            'action_name': action_name,
            'params': params,
            'id': action_id_core
        }
        if action_id_core is None:
            # Then there was a problem sending the action
            response = {
                    'header': 'ACTION RESULT',
                    'message': {
                        'result': 'ERROR: Unable to send action',
                        'metadata': metadata
                    }
            }
        else:
            response = {
                    'header': 'ACTION TICKET',
                    'message': {
                        'result': 'pending',
                        'metadata': metadata
                    }
            }
        return response

    def action_list_handler(self, message):
        header = 'ACTIONS'
        payload = self.client_actions()
        response = {
                'header': header,
                'message': {
                    'result': payload,
                }
        }
        return response


    def handle(self, message):
        logging.debug('Handling message: %s' % message)
        client_id = message[0]
        message_header = message[1]
        if message_header == b'NEW':
            # Register new client
            introduction = protocol.register_intro_parse(message[1:])
            client_name = introduction['name']
            client_shortname = introduction['short_name']
            client_heartbeat_ms = introduction['heartbeat_ms']
            client_connections = introduction['connections']
            client_addresses = introduction['addresses']
            client_actions = introduction['actions']
            self.address_service.update(client_addresses)
            addresses = {}
            has_all_addresses = True
            for connection in client_connections:
                addresses[connection] = self.address_service.get(connection,
                        {})
                if addresses[connection] == {}:
                    has_all_addresses = False
            if not has_all_addresses:
                logging.debug("Haven't received all addresses for client %s",
                        client_name)
                self.addresses_cache[client_id] = addresses
            message = protocol.register_success_create(addresses)
            self.router.send_multipart([client_id] + message)
            client = Client(client_id, client_name, client_shortname,
                    client_heartbeat_ms, client_actions)
            self.clients.append(client)
            if client_heartbeat_ms < self.min_heartbeat_ms:
                self.min_heartbeat_ms = client_heartbeat_ms
            print('Registered new client with name %s' %
                    client_name)
            print('    (id = %s)' % client_id)
            self.log('INFO', 'New client "%s"' % client_name)
            to_remove = []
            for other_client_id in self.addresses_cache:
                addresses = self.addresses_cache[other_client_id]
                if client_shortname in addresses:
                    logging.debug('Sending new address to client %s',
                            other_client_id)
                    addresses[client_shortname] = (
                    self.address_service[client_shortname])
                    message = protocol.register_success_create(addresses)
                    self.router.send_multipart([other_client_id] + message)
                has_all_addresses = True
                for connection in addresses:
                    if addresses[connection] == {}:
                        has_all_addresses = False
                        break
                if has_all_addresses:
                    logging.debug('Removing client %s from address cache',
                            other_client_id)
                    to_remove.append(other_client_id)
            for other_client_id in to_remove:
                del self.addresses_cache[other_client_id]
            for handler in self._event_handlers['new_component']:
                handler.handle(client_name, self.client_list())
        elif message_header == b'PING':  # heartbeat
            client = self.get_client(client_id)
            if client is not None:
                client.update_expiry()
                # respond with a heartbeat
                self.router.send_multipart([client_id, b'PONG'])
        elif message_header == b'CONTROLLER MESSAGE':  # controller
            message_body = protocol.controller_parse(message[1:])
            message_body['_controller_id'] = client_id
            print('Received control message: %s' % message_body)
            if message_body['header'] == 'STATE':
                old_state = self.state
            handler = self.controller_handlers.get(
                    message_body['header'],
                    self.controller_handlers['*'])
            response_raw = handler(message_body)
            if response_raw is not None:
                response = protocol.controller_create(**response_raw)
                self.router.send_multipart([client_id] + response)
            if message_body['header'] == 'STATE':
                new_state = self.state
                for handler in self._event_handlers['state_change']:
                    handler.handle(new_state, old_state)
        elif message_header == b'STATE':
            if message[2] == b'REQUEST':
                self.send_state_update(self.state, client_id)
            else:
                print('Ignoring improper state message: %s' % message)
        elif message_header == b'ACTION':
            result_message = protocol.action_result_parse(message[1:])
            action_id = result_message['id']
            action = self.pending_actions[action_id]
            client_name = action['client_name']
            action_name = action['action_name']
            params = action['params']
            result = result_message['result']
            header = 'ACTION RESULT'
            payload = {
                    'result': result,
                    'metadata': {
                        'client_name': client_name,
                        'action_name': action_name,
                        'params': params,
                        'id': action_id,
                    }
            }
            del self.pending_actions[action_id]
            response = protocol.controller_create(header, payload)
            controller_id = action['_controller_id']
            self.router.send_multipart([controller_id] + response)
            for handler in self._event_handlers['action_complete']:
                handler.handle(client_name, action_name, params, result)
        else:
            print('Ad hoc message received: %s' % message)


class Client(object):
    '''
    Represents a client connected to the Core.

    '''
    def __init__(self, client_id, name, shortname, heartbeat_ms,
            actions):
        self.client_id = client_id
        self.name = name
        self.shortname = shortname
        self.heartbeat_ms = heartbeat_ms
        self.actions = actions
        self.expiry = 0
        self.update_expiry()

    def update_expiry(self):
        self.expiry = time.time() + 5*self.heartbeat_ms*MSEC_TO_SEC
