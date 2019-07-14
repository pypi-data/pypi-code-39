from typing import Any

import requests


def json_request(url: str, method: str = 'GET', headers: dict = None) -> Any:
    request_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if headers:
        request_headers.update(headers)

    return requests.request(url=url, method=method, headers=request_headers).json()
