'''
Base component for xylem components to handle connecting to the system.

'''
from __future__ import absolute_import
from __future__ import print_function

import zmq
import ast
import time
import struct
import threading
import logging
from . import protocol
from .common import MSEC_TO_SEC, SEC_TO_MSEC

def default_parameters():
    obj = {}
    obj['core_address'] = 'tcp://localhost:5551'
    obj['log_address'] = 'tcp://localhost:5678'
    obj['subscription'] = u''
    obj['connect_addresses'] = {}
    obj['connections'] = []
    obj['name'] = 'Default Component'
    obj['group'] = 'DEFAULT'
    obj['action_docs'] = {}
    obj['heartbeat_time_ms'] = 1000
    return obj

class BaseComponent(object):

    COMPONENT_ADDRESS = 'inproc://component'
    def __init__(self, core_address, log_address, subscription,
            name, group, heartbeat_time_ms, connect_addresses,
            connections, action_docs):
        self.context = zmq.Context()
        self.name = name
        self.group = group
        self.addresses = None
        self.connect_addresses = connect_addresses
        self.connections = connections
        self.heartbeat_time_ms = heartbeat_time_ms
        self.action_descriptions = {
                'die': '``die()`` shut down this component',
                'print': '``print([str1, [...]])`` print to console'
        }
        self.action_descriptions.update(action_docs)
        self.actions = {'die': self.die, 'print': print}
        self.heartbeat_bytes = struct.pack('<I', heartbeat_time_ms)
        self.update_heartbeat_at()
        self.update_core_expiry()
        self.state = ''
        self._event_handlers = {
                'data_message': [],
                'info_message': [],
                }
        # Backend sockets (separate daemon thread)
        self.thread = threading.Thread(target=BaseComponent.run_backend,
                args=(self, core_address, log_address, subscription))
        self.thread.start()

        # Frontend socket (main thread)
        self.sockets = []
        self.core = self.context.socket(zmq.PAIR)
        self.sockets.append(self.core)
        self.core.connect(self.COMPONENT_ADDRESS)
        self.log_frontend = self.context.socket(zmq.PUB)
        self.sockets.append(self.log_frontend)
        self.log_frontend.connect(log_address)
        time.sleep(0.1)  # ZeroMQ slow joiner syndrome fix
        self.poller = zmq.Poller()
        self.poller.register(self.core, zmq.POLLIN)
        self.handlers = { self.core: self.handle_core }
        self.request_state()
        logging.debug('Waiting to receive addresses')
        self.log('DEBUG', 'Waiting to receive addresses')
        still_missing_addresses = True
        while self.connections and still_missing_addresses:
            logging.debug('Still don\'t have addresses')
            logging.debug('self.addresses = %s' % self.addresses)
            self.receive(0.1)
            if self.addresses is None: continue
            for connection in connections:
                if self.addresses[connection] == {}:
                    still_missing_addresses = True
                    break
                else:
                    still_missing_addresses = False
        self.log('INFO', 'Successfully connected')

    def addHandler(self, handler):
        '''
        Add the given event handler.

        '''
        event = handler.event
        self._event_handlers[event].append(handler)

    def die(self):
        '''
        Raise an exception.

        '''
        raise RuntimeError('Instructed to die with die method')

    def cleanup(self):
        '''
        Clean up the ZeroMQ instance. Must be called in a ``finally``
        block in the user code.

        '''
        logging.debug('Frontend starting cleanup')
        self.log('INFO', 'Cleaning up')
        for socket in self.sockets:
            socket.close(linger=0)
        logging.debug('Frontend closed all frontend sockets')
        self.context.term()
        logging.debug('Frontend terminated the ZMQ Context')

    def alert_core(self, *messages):
        if self.thread.is_alive():
            self.core.send_multipart(messages)
        else:
            raise RuntimeError('Backend thread is closed')

    def log(self, level, message):
        '''
        Send a log message to the global log.

        '''
        timestamp = time.time()
        component = self.name
        m = protocol.log_create(level, timestamp, component, message)
        self.log_frontend.send_multipart(m)
        return

    def request_state(self):
        '''
        Send the Core a request for the current state.

        '''
        self.core.send_multipart(protocol.state_request_create())

    def receive(self, timeout=0):
        '''
        Receive the next message, up to the given timeout (in seconds).

        '''
        logging.debug('Frontend in receive')
        if timeout:
            timeout_ms = timeout*SEC_TO_MSEC
        else:
            timeout_ms = timeout
        sockets = dict(self.poller.poll(timeout=timeout_ms))
        logging.debug('Frontend finished polling')
        results = []
        for socket in sockets:
            result = self.handlers[socket]()
            if result is not None:
                results.append(result)
        logging.debug('Frontend handled received messages')
        if len(results) > 0:
            self.log('DEBUG', 'Frontend exiting receive '
                    'with results %s...' % str(results)[:20])
        return results

    def handle_core(self):
        '''
        Process the next message arriving from the Core.

        If the message is not generically process-able (i.e. if it is
        specific to a particular component), it will be passed on
        untouched. If it is process-able in its entirety here, it will
        be processed and not passed on. If it is partly process-able
        then that processing will happen and then the message will be
        passed on.

        '''
        logging.debug('Frontend handling message from core')
        self.log('DEBUG', 'Frontend handle_core')
        message_list = self.core.recv_multipart()
        logging.debug('Frontend executed self.core.recv_multipart()')
        logging.debug(message_list)
        if message_list[0] == b'DIE':
            print('FATAL: received DIE message')
            self.log('CRITICAL', 'Received DIE message')
            raise RuntimeError('FATAL: received DIE message')
        elif message_list[0] == b'SUCCESS':
            self.addresses = protocol.register_success_parse(message_list)
            message_list = None
        elif message_list[0] == b'STATE':
                message_body = protocol.state_update_parse(message_list)
                if 'UPDATE' in message_body:
                    new_state = message_body['UPDATE']
                    self.state = new_state
                    message_list = None
        elif message_list[0] == b'ACTION':
            message_body = protocol.action_parse(message_list)
            action_name = message_body['name']
            params = message_body['params']
            self.log('DEBUG', 'Received action %s' % message_body)
            action = self.actions.get(action_name, None)
            if action:
                try:
                    result = action(*params)
                except TypeError as e:
                    logging.exception(e)
                    result = ('ERROR: Invalid parameters %s' % e.args)
                except Exception as e:
                    result = 'ERROR: %s' % e
            else:
                result = ('ERROR: Could not execute action %s' %
                        action_name)
            message_body['result'] = result
            result_message = protocol.action_result_create(
                    message_body['id'],
                    message_body['name'],
                    message_body['params'],
                    message_body['result'],
            )
            self.core.send_multipart(result_message)
        return message_list

    def register_action(self, name, method, docs):
        '''
        Register the given action to this component.

        '''
        self.actions[name] = method
        self.action_descriptions[name] = docs
        return

    def send_action_result(self, action_name, params, result):
        '''
        Send the result of the action back to the Core.

        '''
        message = protocol.action_result_create(action_name, params,
                result)
        self.core.send_multipart(message)

    def run_backend(self, core_address, log_address, subscription):
        '''
        A self-contained broker between the (frontend) component and
        the Core component.

        '''
        backend_sockets = []
        def cleanup_backend(toClose):
            for socket in toClose:
                socket.close(linger=0)
            return
        def send_log_backend(socket, level, message):
            timestamp = time.time()
            component = self.name
            m = protocol.log_create(level, timestamp, component,
                    message)
            socket.send_multipart(m)
            return
        try:
            logging.debug('Entering backend main block')
            core_connection = self.context.socket(zmq.DEALER)
            backend_sockets.append(core_connection)
            component = self.context.socket(zmq.PAIR)
            backend_sockets.append(component)
            log_backend = self.context.socket(zmq.PUB)
            backend_sockets.append(log_backend)
            core_connection.connect(core_address)
            component.bind(self.COMPONENT_ADDRESS)
            log_backend.connect(log_address)
            time.sleep(0.1)  # ZeroMQ slow joiner syndrome fix
            send_log_backend(log_backend, 'DEBUG', 'Backend started up')
            _poller = zmq.Poller()
            _poller.register(core_connection, zmq.POLLIN)
            _poller.register(component, zmq.POLLIN)
            logging.debug('Sending new component registration')
            intro_message = protocol.register_intro_create(
                    self.name, self.group, self.heartbeat_time_ms,
                    self.connections, self.connect_addresses,
                    self.action_descriptions)
            core_connection.send_multipart(intro_message)
            while True:
                if time.time() > self.heartbeat_at:
                    core_connection.send(b'PING')
                    self.update_heartbeat_at()
                if time.time() > self.core_expiry:
                    raise RuntimeError('FATAL: Lost connection to Core')
                sockets = dict(_poller.poll(self.heartbeat_time_ms))
                if core_connection in sockets:
                    message = core_connection.recv_multipart()
                    if message[0] == b'PONG':
                        self.update_core_expiry()
                    elif message[0] == b'SUCCESS':
                        component.send_multipart(message)
                    elif message[0] == b'FAILURE':
                        response = protocol.register_failure_parse(message)
                        error_string = ('FATAL: Core refused connection: %s' %
                                response['reason'])
                        raise RuntimeError(error_string)
                    else:
                        send_log_backend(log_backend, 'DEBUG', 'Passing on '
                                'message to frontend: %s' % message)
                        component.send_multipart(message)
                if component in sockets:
                    message = component.recv_multipart()
                    if message[0] == b'DIE':
                        return
                    core_connection.send_multipart(message)
        except zmq.ZMQError:
            logging.debug('Backend caught ZMQError')
        except:
            logging.debug('Backend caught other exception')
            component.send(b'DIE')
            logging.debug('Backend sent b\'DIE\' to frontend')
            raise
        finally:
            logging.debug('Backend in finally statement')
            cleanup_backend(backend_sockets)
            logging.debug('Backend cleaned up backend sockets')

    def update_heartbeat_at(self):
        self.heartbeat_at = (time.time() +
                self.heartbeat_time_ms*MSEC_TO_SEC)

    def update_core_expiry(self):
        self.core_expiry = (time.time() + 5 *
                self.heartbeat_time_ms*MSEC_TO_SEC)

