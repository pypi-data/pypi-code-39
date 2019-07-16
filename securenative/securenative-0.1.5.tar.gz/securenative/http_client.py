import requests

from securenative.config import sdk_version


class HttpClient:
    def _headers(self, api_key):
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'SecureNative-python',
            'Sn-Version': sdk_version,
            'Authorization': api_key
        }

    def post(self, url, api_key, body):
        return requests.post(url=url, data=body, headers=self._headers(api_key))
