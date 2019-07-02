from urllib.parse import urljoin

from certn import api, requester


class Client(object):
    '''
    Python API client.
    All of the endpoints documented under the ``.api``
    module may be called from a ``.Client`` instance.
    '''

    URL_MAPPING = {'dev': 'demo-api', 'stage': 'demo-api', 'prod': 'api'}

    def __init__(
        self,
        username,
        password,
        environment='dev',
        url=None,
        timeout=requester.DEFAULT_TIMEOUT,
    ):

        self.environment = environment
        self.timeout = timeout
        self.url = f'https://{self.URL_MAPPING[self.environment]}.certn.co'

        if url is not None:
            self.url = url

        # API classes
        self.Auth = api.Auth(self)
        self.Applicants = api.Applicants(self)
        self.Applications = api.Applications(self)
        self.Listings = api.Listings(self)
        self.Properties = api.Properties(self)
        self.Reports = api.Reports(self)

        # Authenticate Client
        self.login(username, password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self, username, password):
        self._username = username
        self._password = password
        self.user_id, self.token = self.Auth.login()

    def logout(self):
        self.Auth.logout()
        self._username = None
        self._password = None
        self.user_id = None
        self.token = None

    def get(self, path, is_json=True, is_authenticated=True):
        '''GET Request with authorization token header'''

        if is_authenticated:
            headers = {'Authorization': f'Token {self.token}'}
            return self._get(path, data='', headers=headers, is_json=is_json)
        else:
            auth = (self._username, self._password)
            return self._get(path=path, data='', is_json=is_json, auth=auth)

    def _get(self, path, data, is_json, headers=None, auth=None):
        '''GET Request to the API'''

        if headers is None:
            headers = {}

        return requester.get_request(
            urljoin(self.url, path),
            data=data,
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            auth=auth,
        )

    def post(self, path, data, is_json=True, is_authenticated=True):
        '''POST Request with authorization token header'''

        if is_authenticated:
            headers = {'Authorization': 'Token {}'.format(self.token)}
            return self._post(path, data, is_json, headers)
        else:
            auth = (self._username, self._password)
            return self._post(path=path, data=data, is_json=is_json, auth=auth)

    def _post(self, path, data, is_json, headers=None, auth=None):
        '''POST Request to the API'''

        if headers is None:
            headers = {}

        return requester.post_request(
            urljoin(self.url, path),
            data=data,
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            auth=auth,
        )

    def put(self, path, data, is_json=True):
        '''PUT Request with authorization token header'''
        headers = {'Authorization': 'Token {}'.format(self.token)}
        return self._put(path, data, is_json, headers)

    def _put(self, path, data, is_json, headers=None, auth=None):
        '''PUT Request to the API'''

        if headers is None:
            headers = {}

        return requester.put_request(
            urljoin(self.url, path),
            data=data,
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            auth=auth,
        )

    def delete(self, path, is_json=True):
        '''DELETE Request with authorization token header'''
        headers = {'Authorization': 'Token {}'.format(self.token)}
        return self._delete(path, data='', headers=headers, is_json=is_json)

    def _delete(self, path, data, is_json, headers=None, auth=None):
        '''PUT Request to the API'''

        if headers is None:
            headers = {}

        return requester.delete_request(
            urljoin(self.url, path),
            data=data,
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            auth=auth,
        )
