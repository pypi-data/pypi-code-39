import json
from datetime import datetime, timedelta

import requests


class AuthenticationError(Exception):
    def __init__(self, details):
        super().__init__("Authentication failed: " + details)


class OpenIDConnect:
    """OpenID connect authentication implementation."""

    _expiration_buffer = 5

    def __init__(self, issuer_url, client_id, client_secret):
        self._issuer_url = issuer_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._configuration = None
        self._access_token = None
        self._access_token_expiration = None
        self._refresh_token = None
        self._refresh_token_expiration = None

    def get_auth_header(self, refresh=False):
        return f"Bearer {self.get_access_token(refresh)}"

    def get_access_token(self, refresh=False):
        if (
            refresh
            or not self._access_token
            or self._access_token_expiration < datetime.utcnow()
        ):
            self._retrieve_access_token()
        return self._access_token

    def get_refresh_token(self, refresh=False):
        if (
            refresh
            or not self._refresh_token
            or self._refresh_token_expiration < datetime.utcnow()
        ):
            self._retrieve_refresh_token()
        return self._refresh_token

    @property
    def configuration(self):
        if not self._configuration:
            response = requests.get(
                url=f"{self._issuer_url}/.well-known/openid-configuration"
            )
            response.raise_for_status()
            self._configuration = response.json()
        return self._configuration

    def _retrieve_refresh_token(self):
        data = (
            "grant_type=client_credentials"
            f"&client_id={self._client_id}"
            f"&client_secret={self._client_secret}"
        )
        header = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url=self.configuration["token_endpoint"], data=data, headers=header
        )
        response.raise_for_status()
        token_data = response.json()
        self._refresh_token = token_data["refresh_token"]
        self._refresh_token_expiration = datetime.utcnow() + timedelta(
            seconds=(token_data["refresh_expires_in"] - self._expiration_buffer)
        )
        if "access_token" in token_data:
            self._access_token = token_data["access_token"]
            self._access_token_expiration = datetime.utcnow() + timedelta(
                seconds=(token_data["expires_in"] - self._expiration_buffer)
            )

    def _retrieve_access_token(self):
        refresh_token = self.get_refresh_token()
        if not self._access_token or self._access_token_expiration < datetime.utcnow():
            data = (
                "grant_type=refresh_token"
                f"&client_id={self._client_id}"
                f"&client_secret={self._client_secret}"
                f"&refresh_token={refresh_token}"
            )
            header = {"content-type": "application/x-www-form-urlencoded"}
            url = self.configuration["token_endpoint"]
            response = requests.post(url=url, data=data, headers=header)
            response.raise_for_status()
            token_data = response.json()
            if "refresh_token" in token_data:
                self._refresh_token = token_data["refresh_token"]
                self._refresh_token_expiration = datetime.utcnow() + timedelta(
                    seconds=(token_data["refresh_expires_in"] - self._expiration_buffer)
                )
            self._access_token = token_data["access_token"]
            self._access_token_expiration = datetime.utcnow() + timedelta(
                seconds=(token_data["expires_in"] - self._expiration_buffer)
            )
