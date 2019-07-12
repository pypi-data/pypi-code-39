import json
import logging
from auth0.v3.authentication import GetToken
import asyncio
import aiohttp


class Onlaw:
    auth_audience = 'https://api.onlaw.dk'
    _token: str = ''
    api_server_aquire_token_lock = asyncio.Lock()

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        domain: str = 'auth.onlaw.dk',
        endpoint: str = 'https://api.onlaw.dk/graphql'
    ):
        self.logger = logging.getLogger(__name__)
        if not client_id or not client_secret:
            raise ValueError('Missing client credentials')

        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_domain = domain
        self.endpoint = endpoint
        self.headers = {
            'Accept': 'application/json',
            'content-type': 'application/json',
        }

    async def execute(self, query: str, session: aiohttp.ClientSession,
                      endpoint: str = None,
                      backoff_interval=1.0, max_retries=10):

        if not endpoint:
            endpoint = self.endpoint

        if not Onlaw._token:
            await self._get_token()

        status = -1

        while status != 200:
            retries = 0
            async with session.post(endpoint, json={'query': query}, headers=self.headers) as response:
                status = response.status

                try:
                    json_response = await response.json(content_type=None)
                    logger_response = json_response
                except json.decoder.JSONDecodeError:
                    logger_response = await response.text()

                if status == 200:
                    return json_response

                self.logger.warning('non successfull post\n {}\n. status: {}'.format(
                    json.dumps(query), status))
                self.logger.warning(
                    'response from server:\n{}'.format(logger_response))

                if status == 401:
                    Onlaw._token = ''
                    await self._get_token()

                if retries > max_retries or self.stop_retries(status):
                    response.raise_for_status()

                sleep_for: int = backoff_interval * retries
                self.logger.warning('Sleeping for {} s and try again'.format(sleep_for))
                await asyncio.sleep(sleep_for)
                retries += 1

    async def _get_token(self):
        async with Onlaw.api_server_aquire_token_lock:
            get_token = GetToken(self.auth_domain, False)

            token_info: dict = get_token.client_credentials(
                client_id=self.client_id,
                client_secret=self.client_secret,
                audience=self.auth_audience,
                grant_type='client_credentials'
            )
            Onlaw._token = token_info['access_token']

            self.headers['Authorization'] = F'Bearer {Onlaw._token}'

    @classmethod
    def stop_retries(cls, status: int) -> bool:
        http_status_codes_no_retries: set = set((400, 404))

        if status in http_status_codes_no_retries:
            return True

        return False
