import hashlib
import hmac
import time
from typing import Dict
from urllib.parse import urlencode

import requests


class LocalBitcoinsError(Exception):
    pass


class Client:
    def __init__(
        self,
        hmac_key: str,
        hmac_secret: str,
        root_addr: str = "https://localbitcoins.com",
    ):
        self._hmac_key = hmac_key
        self._hmac_secret = hmac_secret

        self._root_addr = root_addr

    def _calc_signature(self, nonce: str, endpoint: str, params_encoded: str):
        message = nonce + self._hmac_key + endpoint + params_encoded
        hash_obj = hmac.new(
            self._hmac_secret.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha256,
        )
        sign = hash_obj.hexdigest().upper()

        return sign

    def request(
        self, method: str, endpoint: str, params: Dict[str, str] = None
    ):
        method = method.upper()
        if method not in ("POST", "GET"):
            raise NotImplementedError("Method '%s' not implemented" % method)
        safe_chars = ":" if method == "GET" else ""
        params_encoded = urlencode(
            params, doseq=True, safe=safe_chars, encoding="utf-8"
        )
        nonce = str(int(time.time() * 1000))
        sign = self._calc_signature(nonce, endpoint, params_encoded)

        headers = {
            "Apiauth-Key": self._hmac_key,
            "Apiauth-Nonce": nonce,
            "Apiauth-Signature": sign,
        }
        if method.upper() != "GET":
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        url = self._root_addr + endpoint
        payload_kw = "data" if method == "POST" else "params"
        resp = requests.request(
            method, url, headers=headers, **{payload_kw: params}
        )
        result = resp.json()
        if "error" in result:
            raise LocalBitcoinsError(result["error"])

        return result
