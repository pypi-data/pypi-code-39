import json
import unittest

from securenative.config import sdk_version
from securenative.http_client import HttpClient


class HttpClientTests(unittest.TestCase):
    def test_post(self):
        client = HttpClient()
        api_key = u'ABC'
        request_body = {"key": "test1", "value": "test2"}
        response = client.post(url=u'https://httpbin.org/post', api_key=api_key, body=json.dumps(request_body))

        self.assertEqual(response.status_code, 200)
        json_body = json.loads(response.text)
        self.assertEqual(json_body['headers']['Content-Type'], 'application/json')
        self.assertEqual(json_body['headers']['User-Agent'], 'SecureNative-python')
        self.assertEqual(json_body['headers']['Sn-Version'], sdk_version)
        self.assertEqual(json_body['headers']['Authorization'], api_key)
        self.assertEqual(json_body['json'], request_body)
