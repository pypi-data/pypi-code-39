import asyncio
import functools
import json
import logging
from typing import Optional, Union

import websockets

from .exceptions import *

MAX_PAYLOAD_SIZE_BYTES = 2 ** 23
MAX_PAYLOAD_SIZE_MB=MAX_PAYLOAD_SIZE_BYTES / 1024 ** 2

__all__ = ['Tab']

class GenericAttr(object):

    def __init__(self, name: Union['str'], tab):
        self.__dict__['_name'] = name
        self.__dict__['_tab'] = tab
    
    def __getattr__(self, item):
        method_name = "%s.%s" %(self._name, item)
        event_listener = self._tab.get_listener(method_name)
        if event_listener:
            return event_listener
        return functools.partial(self._tab.call_method, method_name)
    
    def __setattr__(self, key, item):
        self._tab.set_listener("%s.%s" %(self._name, key), item)

    def __delattr__(self, name):
        self._tab.del_listener("%s.%s" %(self._name, name), False)

class Tab(object):
    _title=''
    _url=''
    _ws_uri=''
    _id=''
    _ws: Optional[websockets.WebSocketClientProtocol]=None
    _message_id=0
    _current_task: Optional[asyncio.Task]=None
    _ack_events={}
    _ack_payloads={}
    _recv_task=None
    _log: Union[logging.Logger] = None
    _send_log: Union[logging.Logger] = None
    _recv_log: Union[logging.Logger] = None

    def __init__(self, title: Union['str'], url: Union['str'], ws_uri: Union['str'], tab_id: Optional['str']=None) -> None:
        self._title = title
        self._url = self._url
        self._ws_uri = ws_uri
        if tab_id:
            self._id = tab_id
        else:
            self._id = ws_uri.split('/')[-1]
        self._ws = None
        self._message_id = 0
        self._current_task: Optional[asyncio.Task] = None
        
        self._ack_events = {}
        self._ack_payloads = {}
        self._event_handlers = {}

        self._recv_task = None

        self._log = logging.getLogger('chromemin.tab')
        self._send_log = logging.getLogger('chromemin.tab.send_handle')
        self._recv_log = logging.getLogger('chromemin.tab.recv_handle')

    async def connect(self) -> None:
        self._ws = await websockets.connect(self._ws_uri, max_size=MAX_PAYLOAD_SIZE_BYTES)
        self._recv_task = asyncio.ensure_future(self.recv_handler())
        self._log.info('Connected to Chrome tab %s' %(self._ws_uri))
    
    async def disconnect(self) -> None:
        self._log.debug('DisConnecting tab...')
        if self._current_task and not self._current_task.done() and not self._current_task.cancelled():
            self._log.warning('Cancelling current task for websocket')
            self._current_task.cancelled()
            await self._current_task
        if self._recv_task:
            self._recv_task.cancel()
            await self._recv_task

    def __getattr__(self, item):
        attr = GenericAttr(item, self)
        self._log.debug('tab setattr %s ...' %(item))
        setattr(self, item, attr)
        return attr

    async def recv_handler(self) -> None:
        try:
            while True:
                self._recv_log.debug('Waiting for message...')
                result = await self._ws.recv()
                self._recv_log.debug('Received message, processing...')
                if not result:
                    self._recv_log.error('Missing message, may have been a connection timeout...')
                    continue
                result = json.loads(result)

                if not isinstance(result, dict):
                    self._recv_log.error('decoded message is of type "%s" and = "%s"' %(type(result), result))
                    continue
                
                # message parse
                if 'id' in result:
                    self._ack_payloads[result['id']] = result
                    ack_event = self._ack_events.get(result['id'])
                    if ack_event is None:
                        self._recv_log.error('Ignoring ack with id %s as no registered recv' %(result['id']))
                        continue
                    self._recv_log.debug('Notifying ack event with id=%s' %(result['id']))
                    ack_event.set()
                elif 'method' in result:
                    self._recv_log.debug('Received event message!')
                    event_handler = result['method']
                    if event_handler in self._event_handlers:
                        try:
                            # coroutines
                            asyncio.ensure_future(self._event_handlers[event_handler](**result['params']))
                        except:
                            self._recv_log.error('event callback %s exception' %(event_handler))
                else:
                    self._recv_log.info('Invalid message %s, what do i do now?' % result )
        except asyncio.CancelledError:
            await self._ws.close()

    def get_listener(self, event) -> callable:
        return self._event_handlers.get(event, None)

    def del_listener(self, event=None, complete=False) -> bool:
        if complete is True:
            self._event_handlers = {}
            return True
        elif event:
            if event in self._event_handlers:
                self._event_handlers.pop(event, None)
                return True
            else:
                self._log.error('event_handlers is not define %s' %(event))
                return False
        else:
            raise ValueError

    def set_listener(self, event, callback) -> bool:
        if not callable(callback):
            raise ValueError('callback should be callable')
        self._event_handlers[event] = callback
        return True

    async def _send(self, params, _timeout=5) -> dict:
        self._message_id += 1
        params['id'] = self._message_id

        ack_event = asyncio.Event()
        self._ack_events[self._message_id] = ack_event
        try:
            msg = json.dumps(params, default=lambda obj: obj.__dict__)
            self._send_log.info('Sending command = %s' %(msg))
            self._current_task = asyncio.ensure_future(self._ws.send(msg))
            await asyncio.wait_for(self._current_task, timeout=_timeout)

            self._send_log.debug('Waiting for ack event set for id = %s' %(params['id']))
            await asyncio.wait_for(ack_event.wait(), timeout=_timeout)
            self._send_log.debug('Received ack event set for id = %s' %(params['id']))

            ack_payload = self._ack_payloads[params['id']]
            # delete ram
            self._ack_payloads.pop(params['id'])
            self._ack_events.pop(params['id'])

            if not ack_payload:
                self._send_log.error('Notified but no payload available for id = %s !' %(params['id']))
                return False
            
            error = ack_payload.get('error')
            if error:
                msg = '%s, code %s for id = %s' %(error.get('message', 'Unknown error'), error['code'], params['id'])
                self._send_log.error(msg)
                raise ProtocolError(msg)
            
            return ack_payload['result']
        except asyncio.TimeoutError:
            method = params['method']
            id_ = params['id']
            self._send_log.error(msg)
            if self._ws.closed():
                close_code = self._ws.close_code
                if close_code == 1002:
                    raise ProtocolError('Websocket protocol error occured for "%s" with id=%s' % (method, id_))
                elif close_code == 1006:
                    raise ProtocolError('Incomplete read error occured for "%s" with id=%s' % (method, id_))
                elif close_code == 1007:
                    raise ProtocolError('Unicode decode error occured for "%s" with id=%s' % (method, id_))
                elif close_code == 1009:
                    raise ProtocolError('Recv\'d payload exceeded %sMB for "%s" with id=%s, consider increasing this limit' % (MAX_PAYLOAD_SIZE_MB, method, id_))
            raise TimeoutError('Unknown cause for timeout to occurs for "%s" with id=%s' %(method, id_))
    
    async def call_method(self, _method, *args, **kwargs) -> dict:
        if args:
            raise ValueError('the params should be key=value format')
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if '_timeout' in kwargs:
            timeout = kwargs.pop('_timeout')
            if not timeout and not isinstance(timeout, int) and timeout < 0:
                timeout = 5
        else:
            timeout = 5
        params = {"method": _method, "params": kwargs}
        finished = False
        retries = 0
        max_retries = 3
        while not finished:
            try:
                return await self._send(params, timeout)
            except websockets.exceptions.ConnectionClosed:
                if retries > max_retries:
                    self._log.error('Failed to execute call method %s after %d times!' %(json.dumps(params, default=lambda obj: obj.__dict__), retries))
                    finished = False
                retries += 1
                await self.connect()

    @property
    def title(self):
        return self._title
    
    @property
    def url(self):
        return self._url

    @property
    def ws_uri(self):
        return self._ws_uri
