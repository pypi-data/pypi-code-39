import functools
import os
from typing import Any, Optional

import requests

from tikkie.exceptions import BaseError
from tikkie.types import AccessToken

__version__ = "0.1.0"


USER_AGENT = f"python-tikkie/{__version__}"


AUD_URL = {
    "sandbox": "https://auth-sandbox.abnamro.com/oauth/token",
    "production": "https://auth.abnamro.com/oauth/token",
}

AUTH_URL = {
    "sandbox": "https://auth-sandbox.abnamro.com",
    "production": "https://auth.connect.abnamro.com",
}

API_URL = {"sandbox": "https://api-sandbox.abnamro.com", "production": "https://api.abnamro.com"}

API_KEY_ENV = "TIKKIE_API_KEY"
PRIVATE_KEY_ENV = "TIKKIE_PRIVATE_KEY"
PLATFORM_TOKEN_ENV = "TIKKIE_PLATFORM_TOKEN"


class ApiSession(requests.Session):
    access_token: Optional[AccessToken]

    def __init__(
        self,
        *,
        platform_token: Optional[str] = None,
        api_key: str,
        private_key: str,
        timeout: int = 5,
        sandbox: bool = True,
        **extra_kwargs: Any,
    ):
        super().__init__()
        self.extra_kwargs = extra_kwargs
        self.extra_kwargs["timeout"] = timeout

        self.headers.update(
            {"Accept": "application/json", "User-Agent": f"python-tikkie/{__version__}"}
        )

        self.api_key = api_key
        self.private_key = private_key
        self.base_url = API_URL["sandbox" if sandbox else "production"]
        self.aud_url = AUD_URL["sandbox" if sandbox else "production"]
        self.auth_url = AUTH_URL["sandbox" if sandbox else "production"]
        self.access_token = None
        self.platform_token = platform_token

    def is_authenticated(self) -> bool:
        return self.access_token is not None

    def prepare_request(self, request: Any) -> Any:
        request.url = self.base_url.rstrip("/") + "/" + request.url.lstrip("/")
        return super().prepare_request(request)

    def request(self, *args: Any, **kwargs: Any) -> Any:
        is_auth = kwargs.pop("is_auth", False)
        if not is_auth and not self.is_authenticated():
            from tikkie._api import get_access_token

            self.access_token = get_access_token()
            self.headers.update(
                {
                    "API-Key": self.api_key,
                    "Authorization": f"Bearer {self.access_token.access_token}",
                }
            )

        r = super().request(*args, **{**kwargs, **self.extra_kwargs})
        if not r.ok:
            raise BaseError.from_response(r)
        return r

    def get_platform_token(self, platform_token: Optional[str]) -> str:
        if platform_token is not None:
            return platform_token
        if self.platform_token is not None:
            return self.platform_token
        raise ValueError("platform_token was not passed")


# The global session object
_session: Optional["ApiSession"] = None


def _read_from_os(var: Optional[str], env: str) -> str:
    if var is None:
        var = os.environ.get(env)
        if var is None:
            raise Exception(f"Api not configured, please set the {env} environment variable")
    return var


@functools.lru_cache()
def session() -> ApiSession:
    global _session
    if _session is None:
        configure()
    assert isinstance(_session, ApiSession)
    return _session


def configure(
    *,
    api_key: Optional[str] = None,
    private_key: Optional[str] = None,
    platform_token: Optional[str] = None,
    timeout: Optional[int] = None,
    sandbox: bool = True,
) -> None:
    global _session

    api_key = _read_from_os(api_key, API_KEY_ENV)
    private_key = _read_from_os(private_key, PRIVATE_KEY_ENV)
    platform_token = _read_from_os(platform_token, PLATFORM_TOKEN_ENV)
    # timeout = _read_from_os(timeout, API_URL_ENV)

    session.cache_clear()

    if timeout is None:
        _session = ApiSession(
            api_key=api_key, platform_token=platform_token, private_key=private_key, sandbox=sandbox
        )
    else:
        _session = ApiSession(
            api_key=api_key,
            platform_token=platform_token,
            private_key=private_key,
            timeout=timeout,
            sandbox=sandbox,
        )
