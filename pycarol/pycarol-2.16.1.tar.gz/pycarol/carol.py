from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
import json
import os
import os.path
from .auth.ApiKeyAuth import ApiKeyAuth
from .auth.PwdAuth import PwdAuth
from .tenant import Tenant
from . import __CONNECTOR_PYCAROL__


class Carol:

    def __init__(self, domain=None, app_name=None, auth=None, connector_id=None, port=443, verbose=False):
        """
        This class handle all Carol`s API calls It will handle all API calls,
        for a given authentication method. :param domain: `str`.


        Args:
            domain: `str`. default `None`.
                Tenant name. e.x., domain.carol.ai
            app_name: `str`. default `None`.
                Carol app name.
            auth: `PwdAuth` or `ApiKeyAuth`.
                object Auth Carol object to handle authentication
            connector_id: `str` , default `__CONNECTOR_PYCAROL__`.
                Connector Id
            port: `int` , default 443.
                Port to be used (when running locally it could change)
            verbose: `bool` , default `False`.
                If True will print the header, method and URL of each API call.

        OBS:
            In case all parameters are `None`, pycarol will try yo find their values in the environment variables.
            The values are:
                 1. `CAROLTENANT` for domain
                 2. `CAROLAPPNAME` for app_name
                 3. `CAROLAPPOAUTH` for auth
                 4. `CAROLCONNECTORID` for connector_id

        """


        self.legacy_mode = False
        self.legacy_bucket = 'carol-internal'

        settings = dict()
        if auth is None and domain is None:

            domain = os.getenv('CAROLTENANT')
            app_name = os.getenv('CAROLAPPNAME')

            assert domain and app_name, \
                "One of the following env variables are missing:\n CAROLTENANT: {domain}\n CAROLAPPNAME: {app_name}"

            carol_user = os.getenv('CAROLUSER')
            carol_pw = os.getenv('CAROLPWD')

            if carol_user and carol_pw:
                auth = PwdAuth(user=carol_user, password=carol_pw)

            else:
                auth_token = os.getenv('CAROLAPPOAUTH')
                connector_id = os.getenv('CAROLCONNECTORID')

                assert domain and app_name and auth_token and connector_id,\
                    "One of the following env variables are missing:\n " \
                    f"CAROLTENANT: {domain}\nCAROLAPPNAME: {app_name}" \
                    f"\nCAROLAPPOAUTH: {auth}\nCAROLCONNECTORID: {connector_id}\n"

                auth = ApiKeyAuth(auth_token)


        if connector_id is None:
            connector_id = __CONNECTOR_PYCAROL__


        if domain is None or app_name is None or auth is None:
            raise ValueError("domain, app_name and auth must be specified as parameters, in the app_config.json file " +
                             "or in the environment variables CAROLTENANT, CAROLAPPNAME, CAROLAPPOAUTH" +
                             " OR CAROLUSER+CAROLPWD and " +
                             "CAROLCONNECTORID")

        self.domain = domain
        self.app_name = app_name
        self.port = port
        self.verbose = verbose
        self.tenant = Tenant(self).get_tenant_by_domain(domain)
        self.connector_id = connector_id
        self.auth = auth
        self.auth.set_connector_id(self.connector_id)
        self.auth.login(self)
        self.response = None


    @staticmethod
    def _retry_session(retries=5, session=None, backoff_factor=0.5, status_forcelist=(500, 502, 503, 504, 524),
                       method_whitelist=frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE'])):

        """
        Static method used to handle retries between calls.


        Args:
            retries: `int` , default `5`
                Number of retries for the API calls
            session: Session object dealt `None`
                It allows you to persist certain parameters across requests.
            backoff_factor: `float` , default `0.5`
                Backoff factor to apply between  attempts. It will sleep for:
                        {backoff factor} * (2 ^ ({retries} - 1)) seconds
            status_forcelist: `iterable` , default (500, 502, 503, 504, 524).
                A set of integer HTTP status codes that we should force a retry on.
                A retry is initiated if the request method is in method_whitelist and the response status code is in
                status_forcelist.
            method_whitelist: `iterable` , default frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE']))
                Set of uppercased HTTP method verbs that we should retry on.

        Returns:
            :class:`requests.Section`
        """

        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            method_whitelist=method_whitelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def call_api(self, path, method=None, data=None, auth=True, params=None, content_type='application/json', retries=5,
                 session=None, backoff_factor=0.5, status_forcelist=(502, 503, 504, 524), downloadable=False,
                 method_whitelist=frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE']), errors='raise',
                 extra_headers=None,
                 **kwds):
        """
        This method handles all the API calls.


        Args:
            path: `str`.
                API URI path. e.x.  v2/staging/schema
            method: 'str', default `None`.
                Set of uppercased HTTP method verbs that we should call on.
            data: 'dict`, default `None`.
                Dictionary, list of tuples, bytes, or file-like object to send in
                the body of the request.
            auth: :class: `pycarol.ApiKeyAuth` or `pycarol.PwdAuth`
                Auth type to be used within the API's calls.
            params: (optional) Dictionary, list of tuples or bytes to send
                     in the query string for the :class:`requests.Request`.
            content_type: `str`, default 'application/json'
                Content type for the api call
            retries: `int` , default `5`
                Number of retries for the API calls
            session: :class `requests.Session` object dealt `None`
                It allows you to persist certain parameters across requests.
            backoff_factor: `float` , default `0.5`
                Backoff factor to apply between  attempts. It will sleep for:
                        {backoff factor} * (2 ^ ({retries} - 1)) seconds
            status_forcelist: `iterable` , default (500, 502, 503, 504, 524).
                A set of integer HTTP status codes that we should force a retry on.
                A retry is initiated if the request method is in method_whitelist and the response status code is in
                status_forcelist.
            downloadable: `bool` default `False`.
                If the request will return a file to donwload.
            method_whitelist: `iterable` , default frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE']))
                Set of uppercased HTTP method verbs that we should retry on.
            errors: {‘ignore’, ‘raise’}, default ‘raise’
                If ‘raise’, then invalid request will raise an exception If ‘ignore’,
                then invalid request will return the request response
            extra_headers: `dict` default `None`
                extra headers to be sent.
            kwds: `dixt` default `None`
                Extra parameters to be sent to :class: `requests.request`

        Rerturn:
            Dict with API response.

        """

        extra_headers = extra_headers or {}
        url = 'https://{}.carol.ai:{}/api/{}'.format(self.domain, self.port, path)

        if method is None:
            if data is None:
                method = 'GET'
            else:
                method = 'POST'

        met_list = ['HEAD', 'TRACE', 'GET', 'PUT','POST', 'OPTIONS', 'PATCH',
                    'DELETE', 'CONNECT' ]
        assert method in met_list, f"API method must be {met_list}"

        headers = {'accept': 'application/json'}
        if auth:
            self.auth.authenticate_request(headers)

        data_json = None
        if method == 'GET':
            pass

        elif (method == 'POST') or (method == 'DELETE') or (method == 'PUT'):
            headers['content-type'] = content_type

            if content_type == 'application/json':
                data_json = data
                data = None

        headers.update(extra_headers)
        __count = 0
        while True:
            if session is None:
                session = self._retry_session(retries=retries, session=session, backoff_factor=backoff_factor,
                                              status_forcelist=status_forcelist, method_whitelist=method_whitelist)

            response = session.request(method=method, url=url, data=data, json=data_json,
                                       headers=headers, params=params, **kwds)

            if self.verbose:
                if data_json is not None:
                    print("Calling {} {}. Payload: {}. Params: {}".format(method, url, data_json, params))
                else:
                    print("Calling {} {}. Payload: {}. Params: {}".format(method, url, data, params))
                print("        Headers: {}".format(headers))

            if response.ok or errors == 'ignore':
                if downloadable:  #Used when downloading carol app file.
                    return response

                response.encoding = 'utf-8'
                self.response = response
                if response.text == '':
                    return {}
                return json.loads(response.text)

            elif (response.reason == 'Unauthorized') and isinstance(self.auth,PwdAuth):
                if response.json().get('possibleResponsibleField') in ['password', 'userLogin']:
                    raise Exception(response.text)
                self.auth.get_access_token()  #It will refresh token if Unauthorized
                __count+=1
                if __count<5: #To avoid infinity loops
                    continue
                else:
                    raise Exception('Too many retries to refresh token.\n', response.text)
            raise Exception(response.text)

    def issue_api_key(self):
        """

        Create an API key for a given connector.

        Returns: `dict`
            Dictionary with the API key.

        """
        resp = self.call_api('v2/apiKey/issue', data={
            'connectorId': self.connector_id
        }, content_type='application/x-www-form-urlencoded')
        return resp

    def api_key_details(self, api_key, connector_id):

        """

        Display information about the API key.

        Args:
            api_key: `str`
                Carol's api key
            connector_id: `str`
                Connector Id which API key was created.

        Returns: `dict`
            Dictionary with API key information.

        """

        resp = self.call_api('v2/apiKey/details',
                             params = {"apiKey": api_key,
                                            "connectorId": connector_id})

        return resp

    def api_key_revoke(self, connector_id):

        """

        Args:
            connector_id: `str`
                Connector Id which API key was created.
        Returns: `dict`
            Dictionary with API request response.

        """

        resp = self.call_api('v2/apiKey/revoke', method='DELETE',
                             content_type='application/x-www-form-urlencoded',
                             params = {"connectorId": connector_id})

        return resp

    def copy_token(self):
        import pyperclip
        if isinstance(self.auth, PwdAuth):
            token = self.auth._token.access_token
            pyperclip.copy(token)
            print("Copied auth token to clipboard: " + token)
        elif isinstance(self.auth, ApiKeyAuth):
            token = self.auth.api_key
            pyperclip.copy(token)
            print("Copied API Key to clipboard: " + token)
        else:
            raise Exception("Auth object not set. Can't fetch token.")


