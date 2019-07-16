import functools
import json
import threading
import unittest

from securenative import Event, event_types
from securenative.event_manager import EventManager
from securenative.event_options import User, CustomParam


class EventManagerTests(unittest.TestCase):

    def build_event(self):
        return Event(event_type=event_types.login, user=User(user_id='1', user_email='1@2.com', user_name='1 2'),
                     params=[CustomParam('key', 'val')])

    def test_send_sync(self):
        api_key = 'key'
        resource = 'my/custom/resource'
        client = HttpClientMock(None)
        event = self.build_event()
        manager = EventManager(api_key=api_key, http_client=client)
        url, key, body = manager.send_sync(event, resource)

        self.assertEqual(url, 'https://api.securenative.com/' + resource)
        self.assertEqual(key, api_key)
        self.assertEqual(body, json.dumps(event.as_dict()))

    def test_send_async(self):
        wg = threading.Event()
        api_key = 'key'
        resource = 'my/custom/resource'
        event = self.build_event()
        client = HttpClientMock(functools.partial(self.assert_cb, wg, event))

        manager = EventManager(api_key=api_key, http_client=client)
        manager.send_async(event, resource)
        self.assertTrue(wg.wait(manager.options.interval//1000 * 2))

    def assert_cb(self, wg, event, url, key, body):
        self.assertEqual(url, 'https://api.securenative.com/my/custom/resource')
        self.assertEqual(key, 'key')
        self.assertEqual(body, json.dumps(event.as_dict()))
        wg.set()


class HttpClientMock(object):
    def __init__(self, cb):
        self.cb = cb

    def post(self, url, api_key, body):
        if self.cb is not None:
            self.cb(url, api_key, body)
        return url, api_key, body
