from concurrent import futures
from json.decoder import JSONDecodeError

from requests import (
    session, ReadTimeout, ConnectionError
)


def serialize(data, required):
    if required is True and isinstance(data, dict):
        error = data.get('error', None)
        if error:
            code = data.get('code', None)
            if code == 429:
                return None
    return data


class HitBTC:

    def __init__(self, public: str, secret: str, version: int = 2, thread: bool = False):
        self.URL = 'https://api.hitbtc.com'
        self.API_V1 = '/api/1'
        self.API_V2 = '/api/2'
        self.THREAD = thread
        self.PUBLIC = public
        self.SECRET = secret

        self.params = dict()
        self.request = session()
        self.request.auth = (self.PUBLIC, self.SECRET)

        if version == 1:
            self.URL += self.API_V1
        elif version == 2:
            self.URL += self.API_V2

    def send(self, method: str, endpoint: str, params: dict = None) -> object:
        if self.request:
            connection = getattr(self.request, method.lower())

            def _request():
                response = connection('%s/%s' % (self.URL, endpoint), params=params, data=params).json()
                if isinstance(response, dict):
                    error = response.get('error', None)
                    if error:
                        error = {
                            'error': True, **error
                        }
                        return error
                return response

            def _thread():
                with futures.ThreadPoolExecutor(max_workers=5) as executor:
                    future = {executor.submit(_request)}
                    for future in futures.as_completed(future):
                        return future.result()

            try:
                if self.THREAD is True:
                    return _thread()
                return _request()
            except (ReadTimeout, ConnectionError):
                if self.THREAD is True:
                    return _thread()
                return _request()
            except JSONDecodeError:
                pass
