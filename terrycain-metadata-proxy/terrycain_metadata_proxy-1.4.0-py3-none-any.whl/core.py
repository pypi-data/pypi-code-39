import asyncio
import os
import json
import datetime
import logging
from typing import Union, Dict, Tuple, Optional

import aiohttp
import dateutil.parser
import pytz
import netifaces

logger = logging.getLogger('metadata-proxy.core')


UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', '120'))
CONFIG_FILE = 'config.json'

METADATA_DEFAULTS = {
    'ami-id': 'ami-12345678',
    'ami-launch-index': '0',
    'ami-manifest-path': '(unknown)',
    'reservation-id': 'r-fea54097',
    'local-hostname': 'ip-172-0-0-1',
    'local-ipv4': '172.0.0.1',
    'hostname': 'ip-172-0-0-1',
    'instance-action': 'none',
    'instance-id': 'i-0123456789abcdef0',
    'instance-type': 'c5.16xlarge',
    'availability-zone': 'eu-west-9z',
    'profile': 'default-hvm',
    'public-keys': [],  # [['prod-key', 'ssh-rsa ...']]  public-keys/0/openssh-key
    'registered-state': 'unregistered'
}


class BaseCore(object):
    def __init__(self) -> None:
        self._proxy = self._get_proxy()

        # _config['metadata'] = {} the keys in this dict match exactly that in the metadata api list
        self._config = {}

    @staticmethod
    def _get_proxy() -> Optional[str]:
        # aiohttp doesnt support https:// proxy urls, so https proxy urls will be converted
        if 'HTTP_PROXY' in os.environ:
            proxy = os.environ['HTTP_PROXY']
        elif 'HTTPS_PROXY' in os.environ:
            proxy = os.environ['HTTPS_PROXY'].replace('https', 'http')
        else:
            proxy = None

        if proxy and not proxy.startswith('http'):
            proxy = 'http://' + proxy

        return proxy

    def load_config(self) -> None:
        pass

    def save_config(self) -> None:
        pass

    async def setup(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def update_loop(self) -> None:
        pass

    async def update(self) -> None:
        pass

    async def get_host_credentials(self, role: str) -> Tuple[int, str]:
        pass

    async def register_proxy(self, server_url: str, registration_key: str, skip_if_registered: bool = False) -> Tuple[int, str]:
        pass

    @property
    def aws_metadata(self) -> Dict[str, str]:
        return self._config['metadata']

    @property
    def iam_role(self) -> None:
        return self._config.get('role')

    @property
    def api_key(self) -> Union[str, None]:
        return self._config.get('key')

    @property
    def update_url(self) -> Union[str, None]:
        return self._config.get('update_url')

    @property
    def sts_url(self) -> Union[str, None]:
        return self._config.get('sts_url')

    @property
    def ecs_url(self) -> Union[str, None]:
        return self._config.get('ecs_url')


class Core(BaseCore):
    def __init__(self, config_file: str = CONFIG_FILE) -> None:
        super(Core, self).__init__()
        self._config_file = config_file

        self._update_loop_future = None
        self._aiohttp_session = None
        self.last_updated_config = None

        # Store current role creds in memory but if we restart we can get them again
        self._creds = {}

    def load_config(self) -> None:
        if os.path.exists(self._config_file):
            logger.debug('Loading config')
            with open(self._config_file) as open_file:
                self._config = json.load(open_file)

        else:
            self._config['metadata'] = {}

        # When we're initially starting up unregistered, provision the metadata with some random defaults
        for key, value in METADATA_DEFAULTS.items():
            if key not in self._config['metadata']:
                self._config['metadata'][key] = value

    def save_config(self) -> None:
        logger.debug('Saving config')
        # Create a file initially with permissions only we can read from
        with os.fdopen(os.open(self._config_file, os.O_WRONLY | os.O_CREAT, 0o600), 'w') as open_file:
            json.dump(self._config, open_file)

    async def setup(self) -> None:
        self.load_config()

        # Initialise a client session within an async task
        self._aiohttp_session = aiohttp.ClientSession()

        # Start a loop that will regularly ping for updates
        self._update_loop_future = asyncio.ensure_future(self.update_loop())

    async def close(self) -> None:
        self._update_loop_future.cancel()
        await self._update_loop_future

        await self._aiohttp_session.close()

    async def update_loop(self) -> None:
        logger.info('Update loop starting')
        while True:
            try:
                if self.api_key and self.update_url:
                    await self.update()

                await asyncio.sleep(UPDATE_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as err:
                logger.exception('Exception in update loop'.format(err), exc_info=err)
        logger.info('Update loop stopped')

    async def update(self) -> None:
        try:
            async with self._aiohttp_session.get(
                    self.update_url,
                    headers={'Authorization': 'Token {0}'.format(self.api_key)},
                    proxy=self._proxy) as resp:
                if resp.status == 200:
                    json_data = await resp.json()

                    new_config = {
                        'key': json_data['key'],
                        'role': json_data['role'],
                        'update_url': json_data['update_url'],
                        'sts_url': json_data['sts_url'],
                        'ecs_url': json_data['ecs_url'],
                        'metadata': json_data['metadata']
                    }
                    new_config['metadata']['registered-state'] = 'registered'
                    self._config = new_config
                    self.save_config()
                    logger.debug('Updated successfully')
                    self.last_updated_config = datetime.datetime.utcnow()
                else:
                    text = await resp.text()
                    logger.error('Failed to update, status={0}, text={1}'.format(resp.status, text))
        except Exception as err:
            logger.error('Failed to update, error: {0}'.format(err))

    async def get_host_credentials(self, role: str) -> Tuple[int, str]:
        # The server returns the JSON that the credential endpoint from the metadata API would

        # Do some pre_caching
        # dateutil returns a timezone aware datetime, so we get utcnow and use that
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if role in self._creds:
            # Only 3.7+ has .fromisoformat
            expire_minus5 = dateutil.parser.parse(self._creds[role]['Expiration']) - datetime.timedelta(minutes=5)
            # If now is before (less than) the expiry minus 5 mins, then use cached credentials
            if now < expire_minus5:
                text = json.dumps(self._creds, indent=2)
                return 200, text

        try:
            async with self._aiohttp_session.get(
                    self.sts_url,
                    headers={'Authorization': 'Token {0}'.format(self.api_key)},
                    proxy=self._proxy) as resp:

                if resp.status == 200:
                    logger.info('Host IAM credential request successful')
                    json_data = await resp.json()
                    self._creds[role] = json_data

                    # The AWS endpoint returns the json with an indent of 2
                    text = json.dumps(json_data, indent=2)
                    return 200, text
                elif resp.status == 400:
                    return 404, ''

                text = await resp.text()
                logger.error('Unknown status code: {0}, text: {1}'.format(resp.status, text))
                return 500, 'Unknown error occurred whilst getting credentials'
        except Exception as err:
            logger.error('Failed to register, error: {0}'.format(err))
            return 500, 'Failed to get credentials from server: {0}'

    async def register_proxy(self, server_url: str, registration_key: str, skip_if_registered: bool = False) -> Tuple[int, str]:
        # Find IPv4 address
        try:
            default_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
            ipv4 = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['addr']
        except Exception as err:
            logger.exception('Failed to get IPv4 address, cannot register', exc_info=err)
            return 500, json.dumps({'error': True, 'reason': 'Failed to get IPv4 address', 'exception': str(err)})

        # Quit now if we're already registered and skip if registered
        if self.aws_metadata['registered-state'] == 'registered' and skip_if_registered:
            logger.info('Already registered, skipping')
            return 200, json.dumps({'error': False})

        payload = {
            'key': registration_key,
            'ipv4': ipv4,
            'hostname': os.uname()[1]
        }

        # Send registration request to server
        try:
            async with self._aiohttp_session.post(server_url, json=payload, proxy=self._proxy) as resp:
                json_data = await resp.json()
        except Exception as err:
            # Not using logger.exception as currently will spam multiline stack trace (undo if json logging is added)
            logger.error('Failed to register, error: {0}'.format(err))
            return 500, json.dumps({'error': True, 'reason': 'Failed to get register to server: {0}'.format(err), 'upstream_error': None})

        if resp.status != 200:
            logger.error('Registration failed, status code: {0}, reason: {1}'.format(resp.status, json_data.get('reason', 'No reason supplied')))
            return 500, json.dumps({'error': True, 'reason': 'Failed to get register to server', 'upstream_error': json_data.get('reason', 'No reason supplied')})

        # Update config
        new_config = {
            'key': json_data['key'],
            'role': json_data['role'],
            'update_url': json_data['update_url'],
            'sts_url': json_data['sts_url'],
            'ecs_url': json_data['ecs_url'],
            'metadata': json_data['metadata']
        }
        new_config['metadata']['registered-state'] = 'registered'
        self._config = new_config
        self.save_config()
        self.last_updated_config = datetime.datetime.utcnow()
        logger.info('Registered successfully')
        return 200, json.dumps({'error': False})

