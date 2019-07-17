'''
The Controller component allows humans to interact with the DAQ system, e.g.
by sending commands to components or requesting the list of connected
components.

It is a special component in that it only communicates with the Core and
does not represent part of the data flow.

'''
from __future__ import absolute_import
from __future__ import print_function
import os
if 'EVENTLET' in os.environ:
    import eventlet.green.zmq as zmq
else:
    import zmq
import time
import logging
from . import protocol
from .common import SEC_TO_MSEC

class Controller(object):
    def __init__(self, core):
        self.context = zmq.Context()
        self.core = self.context.socket(zmq.DEALER)
        self.core.connect(core)
        self.actions_by_number = None
        self.available_actions_cache = None
        self.pending_action = None

    def cleanup(self):
        self.core.close(linger=0)
        self.context.term()

    def receive(self, timeout=0):
        if timeout is not None:
            timeout_ms = timeout*SEC_TO_MSEC
        else:
            timeout_ms = -1  # block indefinitely
        try:
            self.core.setsockopt(zmq.RCVTIMEO, timeout_ms)
            message_raw = self.core.recv_multipart()
            return self.handle_controller_message(message_raw)
        except ZMQError:
            return None

    def handle_controller_message(self, message):
        message_body = protocol.controller_parse(message)
        payload = message_body['message']
        header = message_body['header']
        if header == 'CLIENTS':
            toPrint = ', '.join(payload)
        elif header == 'STATE':
            toPrint = payload
        elif header == 'ACTIONS':
            toPrint = self.format_actions(payload)
            self.available_actions_cache = payload
        elif header == 'ACTION TICKET':
            action_id = payload['metadata']['id']
            action_data = self.pending_action
            action_data.update(payload)
            toPrint = action_data
        elif header == 'ACTION RESULT':
            action_id = payload['metadata']['id']
            action_data = self.pending_action
            action_data.update(payload)
            toPrint = action_data
        else:
            toPrint = payload
        logging.debug('%s: %s' % (header, toPrint))
        return message_body

    def send_message(self, header, message):
        alert = protocol.controller_create(header, message)
        self.core.send_multipart(alert)

    def request_clients(self):
        self.send_message('CLIENTS', '')

    def request_state(self):
        self.send_message('STATE REQUEST', '')

    def request_state_change(self, new_state):
        self.send_message('STATE', new_state)

    def send_action(self, client_name, action_name, params):
        payload = {
                'client_name': client_name,
                'action_name': action_name,
                'params': params,
        }
        self.send_message('ACTION', payload)
        payload['timestamp'] = time.time()
        self.pending_action = payload

    def request_actions(self):
        self.send_message('ACTIONS', '')

    def format_actions(self, actions):
        '''
        Format the actions in a user-friendly way and return a string.

        '''
        self.actions_by_number = {}
        result = ''
        i = 1
        for component, action_docs in actions.items():
            result += component + '\n'
            for action, doc in action_docs.items():
                result += ' %d' % i
                result += '    '
                result += action
                result += ': '
                result += doc
                result += '\n'
                self.actions_by_number[i] = (component, action, doc)
                i += 1
        return result
