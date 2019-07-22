# -*- coding: utf-8 -*-

"""API module."""

import requests
import logging
import responses


LOGGER = logging.getLogger(__name__)


class APIClient:
    def __init__(self, api_url):
        self.api = api_url

    def __request(self, method: str, endpoint: str):
        url = self.api + endpoint
        LOGGER.debug(f"{method}::{url}")
        return requests.request(method, url)

    def get(self, endpoint):
        return self.__request("GET", endpoint)


class APIFixture:
    def __init__(self, api_url):
        self.api = api_url

    @responses.activate
    def get(self, endpoint, response_status=200, response_body=None):
        url = self.api + endpoint
        responses.add(responses.GET, url, status=response_status, json=response_body)
        response = requests.get(url)
        return response


class APIClientFactory:
    @staticmethod
    def get_api(api_url, mode="generic"):
        flavours = {"generic": APIClient, "fixture": APIFixture}
        return flavours[mode](api_url)
