import logging
from contextlib import contextmanager
from typing import Callable
from typing import Dict
from typing import Optional

import requests
from requests import ConnectionError
from requests import Session
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from urllib3.exceptions import ClosedPoolError

from propileu_sdk.config import HOST
from propileu_sdk.config import HOST_AUTH
from propileu_sdk.config import PASSWORD
from propileu_sdk.config import REQUESTS_MAX_RETRIES
from propileu_sdk.config import REQUESTS_TIMEOUT
from propileu_sdk.config import USERNAME
from propileu_sdk.entities.exceps import AuthenticationFatalErrorException
from propileu_sdk.entities.exceps import CouldNotCompleteAuthenticationException
from propileu_sdk.entities.exceps import PropileuApiBrokenIntegrationException
from propileu_sdk.entities.exceps import PropileuApiInvalidRequestException
from propileu_sdk.entities.exceps import PropileuSdkNotProperlyConfiguredException

logging.info(f"Retries configured: {REQUESTS_MAX_RETRIES}")
logging.info(f"Timeout configured: {REQUESTS_TIMEOUT}")


class AuthenticationLogic(AuthBase):
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.token = None

    def __call__(self, request):
        request.headers["Authorization"] = f"Token {self._get_configured_token()}"
        return request

    def _get_configured_token(self):
        if self.token is None:
            self.token = self._get_token_from_server()
        return self.token

    def _get_token_from_server(self):
        data = {"username": self.username, "password": self.password}
        response = requests.post(self.address, json=data, timeout=REQUESTS_TIMEOUT)
        if response.status_code == 200:
            logging.debug(f"Authenticated! Retrieving token...")
            payload = response.json()
            return payload["token"]
        elif response.status_code == 400:
            logging.error(f"Authentication not established. Details: {response.text}")
            raise CouldNotCompleteAuthenticationException()
        else:
            logging.error(f"Unknown error caught. Status code: {response.status_code}. Details: {response.text}")
            raise AuthenticationFatalErrorException()

    def reconfigure_token(self):
        self.token = self._get_token_from_server()


_custom_adapter = HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES)
_authentication_logic = AuthenticationLogic(f"{HOST_AUTH}", USERNAME, PASSWORD)


@contextmanager
def _get_client() -> Session:
    if not (HOST_AUTH and HOST and USERNAME and PASSWORD):
        raise PropileuSdkNotProperlyConfiguredException()
    session = requests.Session()
    session.mount("https://", _custom_adapter)
    session.mount("http://", _custom_adapter)
    default_headers = session.headers
    default_headers["Connection"] = "Close"
    session.auth = _authentication_logic
    try:
        yield session
    finally:
        session.close()


def _execute(request_to_be_executed: Callable):
    max_tries = 3
    tries = 0
    while True:
        response = request_to_be_executed()
        if response.status_code == 401:
            logging.info(f"Asking to reauthenticate. Attempt {tries}")
            _authentication_logic.reconfigure_token()
        # TODO: Maybe pass this control to the caller
        if response.status_code in (200, 201):
            return response
        if tries >= max_tries:
            break
        tries += 1
    return response


def _retry_if_especial_exception_is_caught(execution_to_be_callable: Callable):
    max_tries = 5
    tries = 0
    while True:
        try:
            response = execution_to_be_callable()
            return response
        except (ClosedPoolError, ConnectionError) as e:
            logging.warning(f"Exception of type {type(e)} was caught. Attempt {tries} of {max_tries}...")
            if tries >= max_tries:
                raise e
            tries += 1


class BaseManager:
    def __init__(self, request_id: Optional[str] = None):
        self.request_id = request_id

    def execute_get(self, request_path: str, params: Optional[Dict] = None) -> Optional[Dict]:
        def _get_logic():
            with _get_client() as client:
                url = f"{HOST}{request_path}"
                response = _execute(
                    lambda: client.get(url, headers=self._get_headers(), timeout=REQUESTS_TIMEOUT, params=params)
                )
                if response.status_code in (400, 401, 403):
                    raise PropileuApiInvalidRequestException(
                        f"Status code {response.status_code} with: {response.text}"
                    )
                if response.status_code == 404:
                    logging.debug("Resource not found: %s", url)
                    return None
                if response.status_code == 200:
                    return response.json()

                raise PropileuApiBrokenIntegrationException(f"Status code {response.status_code} with: {response.text}")

        return _retry_if_especial_exception_is_caught(_get_logic)

    def execute_post(self, request_path: str, data: dict) -> Optional[Dict]:
        def _post_logic():
            with _get_client() as client:
                url = f"{HOST}{request_path}"
                response = _execute(
                    lambda: client.post(url, json=data, headers=self._get_headers(), timeout=REQUESTS_TIMEOUT)
                )
                if response.status_code in (400, 401, 403):
                    raise PropileuApiInvalidRequestException(
                        f"Status code {response.status_code} with: {response.text}"
                    )
                if response.status_code == 404:
                    logging.debug("Resource not found: %s", url)
                    return None
                if response.status_code == 201:
                    return response.json()

                raise PropileuApiBrokenIntegrationException(f"Status code {response.status_code} with: {response.text}")

        return _retry_if_especial_exception_is_caught(_post_logic)

    def execute_put(self, request_path: str, data: dict) -> Optional[Dict]:
        def _put_logic():
            with _get_client() as client:
                url = f"{HOST}{request_path}"
                response = _execute(
                    lambda: client.put(url, json=data, headers=self._get_headers(), timeout=REQUESTS_TIMEOUT)
                )
                if response.status_code in (400, 401, 403):
                    raise PropileuApiInvalidRequestException(
                        f"Status code {response.status_code} with: {response.text}"
                    )
                if response.status_code == 404:
                    logging.debug("Resource not found: %s", url)
                    return None
                if response.status_code == 200:
                    return response.json()

                raise PropileuApiBrokenIntegrationException(f"Status code {response.status_code} with: {response.text}")

        return _retry_if_especial_exception_is_caught(_put_logic)

    def _get_headers(self) -> dict:
        return {"Content-Type": "application/json", "X-REQUEST-ID": self.request_id}
