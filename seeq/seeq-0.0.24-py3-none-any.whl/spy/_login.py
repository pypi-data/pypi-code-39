import logging
import os
import six
import urllib
import urllib3

from seeq.base import gconfig
from seeq.sdk import *
from seeq.sdk.rest import ApiException

from urllib3.connectionpool import MaxRetryError

client = None  # type: ApiClient
user = None  # type: UserOutputV1


def login(username=None, password=None, url=None, auth_provider='Seeq', ignore_ssl_errors=False, credentials_file=None):
    # Annoying warnings are printed to stderr if connections fail
    logging.getLogger("requests").setLevel(logging.FATAL)
    logging.getLogger("urllib3").setLevel(logging.FATAL)
    urllib3.disable_warnings()

    if url:
        parsed_url = urllib.parse.urlparse(url)
        gconfig.override_global_property('seeq_server_hostname', parsed_url.hostname)
        if parsed_url.scheme == 'https':
            port = '443'
            if parsed_url.port:
                port = six.text_type(parsed_url.port)
            gconfig.override_global_property('seeq_server_port', '')
            gconfig.override_global_property('seeq_secure_port', port)
        if parsed_url.scheme == 'http':
            port = '80'
            if parsed_url.port:
                port = six.text_type(parsed_url.port)
            gconfig.override_global_property('seeq_server_port', port)
            gconfig.override_global_property('seeq_secure_port', '')

    api_client_url = gconfig.get_api_url()

    cert_file = os.path.join(gconfig.get_data_folder(), 'keys', 'seeq-cert.pem')
    if os.path.exists(cert_file):
        Configuration().cert_file = cert_file
    key_file = os.path.join(gconfig.get_data_folder(), 'keys', 'seeq-key.pem')
    if os.path.exists(key_file):
        Configuration().key_file = key_file

    Configuration().verify_ssl = not ignore_ssl_errors

    global client
    client = ApiClient(api_client_url)

    auth_api = AuthApi(client)
    auth_input = AuthInputV1()

    if credentials_file:
        try:
            with open(credentials_file) as f:
                lines = f.readlines()
        except Exception as e:
            raise RuntimeError('Could not read credentials_file "%s": %s' % (credentials_file, e))

        if len(lines) < 2:
            raise RuntimeError('credentials_file "%s" must have two lines: username then password')

        username = lines[0].strip()
        password = lines[1].strip()

    if not username or not password:
        raise RuntimeError('Both username and password must be supplied')

    auth_input.username = username
    auth_input.password = password

    auth_providers = dict()
    try:
        auth_providers_output = auth_api.get_auth_providers()  # type: AuthProvidersOutputV1
    except MaxRetryError as e:
        raise RuntimeError(
            '"%s" could not be reached. Is the server or network down?\n%s' % (api_client_url, e))

    for datasource_output in auth_providers_output.auth_providers:  # type: DatasourceOutputV1
        auth_providers[datasource_output.name] = datasource_output

    if auth_provider not in auth_providers:
        raise RuntimeError('auth_provider "%s" not recognized. Possible auth_provider(s) for this server: %s' %
                           (auth_provider, ', '.join(auth_providers.keys())))

    datasource_output = auth_providers[auth_provider]
    auth_input.auth_provider_class = datasource_output.datasource_class
    auth_input.auth_provider_id = datasource_output.datasource_id

    try:
        auth_api.login(body=auth_input)
    except ApiException as e:
        if e.status == 401:
            raise RuntimeError(
                '"%s" could not be logged in with supplied credentials, check username and password.' %
                auth_input.username)
        else:
            raise
    except MaxRetryError as e:
        raise RuntimeError(
            '"%s" could not be reached. Is the server or network down?\n%s' % (api_client_url, e))
    except Exception as e:
        raise Exception('Could not connect to Seeq"s API at %s with login "%s".\n%s' % (api_client_url,
                                                                                        auth_input.username, e))

    users_api = UsersApi(client)

    global user
    user = users_api.get_me()
