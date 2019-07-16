import unittest
import os
import uuid
from time import sleep

import securenative
from securenative import SecureNativeOptions
from securenative.event_options import CustomParam, User, Event


class IntegrationTest(unittest.TestCase):
    def test_integration_with_server(self):
        api_key = os.environ.get('TEST_API_KEY')
        user_id = str(uuid.uuid4())

        options = SecureNativeOptions(auto_send=False)
        securenative.init(api_key, options)

        securenative.track(self.build_event(user_id, securenative.event_types.login, '52.23.233.3'))
        securenative.flush()
        sleep(10)
        result = securenative.verify(self.build_event(user_id, securenative.event_types.verify, '31.168.11.138'))

        self.assertEqual(result['riskLevel'], 'high')
        self.assertEqual(result['score'], 0.64)
        self.assertIsNotNone(result['triggers'])

    def build_event(self, id, type, ip):
        return Event(event_type=type,
                     ip=ip,
                     user=User(user_id=id, user_email='python-sdk@securenative.com', user_name='python sdk'),
                     params=[CustomParam('key', 'val')]
                     )
