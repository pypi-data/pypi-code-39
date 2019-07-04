#
#   Written by ThousandEyes Professional Services.
#   Email services@thousandeyes.com
#   License is covered under the existing MSA agreement between customer and ThousandEyes
#

import logging
import json
import base64
import time
import math
import threading

import certifi
import urllib3
from urllib.parse import urlencode


class Network:
    """
    Class for network, API connections to ThousandEyes
    """

    api_version = "v6"
    api_req_limit = 10
    url = "api.thousandeyes.com"
    retries = 10

    def __init__(
        self,
        username,
        authToken,
        authType=None,
        timeout=None,
        network_httpsConnPoolSize=None,
        proxy_username=None,
        proxy_password=None,
        proxy_address=None,
        proxy_type=None,
    ):

        self.username = username
        self.authToken = authToken
        self.timeout = timeout
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.proxy_address = proxy_address
        self.proxy_type = proxy_type

        self.__rate_limit = 1
        self.__rate_limit_remaining = 1
        self.__rate_limit_reset = 0
        self.__rate_limit_hard_keep = (
            0.05
        )  # Always keep 5% of calls in the end, this is dynamic and
        # increases for 2% with each 429, up to 30%
        self.__rate_limit_hard_keep_update = (
            0
        )  # Ensures __rate_limit_hard_keep is only increased once per rate period

        if authType is None:
            self.authType = "basic"
        else:
            self.authType = authType

        self.https_pool = None

        if network_httpsConnPoolSize is None:
            self.httpsConnPoolSize = 150
        else:
            self.httpsConnPoolSize = network_httpsConnPoolSize

        headers = None
        if self.authType == "basic" or self.authType is None:
            headers = self.__headers(
                self.username, self.authToken, self.proxy_username, self.proxy_password
            )
        elif self.authType == "oauth":
            headers = {"Authorization": "bearer " + self.authToken}

        try:
            if self.proxy_address is not None and self.proxy_type is not None:
                from urllib3 import make_headers

                proxy_headers = None
                if self.proxy_username is not None and self.proxy_password is not None:
                    proxy_headers = make_headers(
                        proxy_basic_auth=self.proxy_username + ":" + self.proxy_password
                    )

                if self.proxy_type == "http":
                    self.https_pool = urllib3.ProxyManager(
                        self.proxy_address,
                        maxsize=self.httpsConnPoolSize,
                        timeout=self.timeout,
                        proxy_headers=proxy_headers,
                        headers=headers,
                        cert_reqs="CERT_REQUIRED",
                        ca_certs=certifi.where(),
                        retries=self.retries,
                        block=True,
                    )
            else:
                # create thread-safe pool of connections to api.thousandeyes.com
                self.https_pool = urllib3.HTTPSConnectionPool(
                    self.url,
                    port=443,
                    timeout=self.timeout,
                    headers=headers,
                    maxsize=self.httpsConnPoolSize,
                    cert_reqs="CERT_REQUIRED",
                    ca_certs=certifi.where(),
                    retries=self.retries,
                    block=True,
                )
        except Exception as exception:
            logging.exception("Network.__init__() - Exception raised: %s" % exception)

    def test_te_connection(self):
        """
        Purpose: test connection to ThousandEyes /status.json API
        Inputs: None
        Returns: True on success, False on failure
        """
        try:
            req = self.https_pool.request(
                "GET", "https://" + self.url + "/" + self.api_version + "/status.json"
            )

        except Exception as exception:
            logging.exception(
                "Network:test_te_connection() - Exception raised: %s" % exception
            )
            return False

        if (req is not None) and (req.status == 200):
            js_time = json.loads(req.data.decode("utf-8"))
            controller_time = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(js_time.get("timestamp") / 1000)
            )
            logging.debug(
                "Network:test_te_connection:: Test successful, controller_time: %s"
                % controller_time
            )
            return True

        return False

    def get(self, query, options=None, data_type="json"):
        """
        Purpose: performs https get request from ThousandEyes API
        Inputs:
            query: API query string
            options: HTTP options
            data_type: JSON (default), or XML (if overriden)
        Returns:
            Response or None
        """

        if self.https_pool is None:
            headers = None

            if self.authType == "basic" or self.authType is None:
                headers = self.__headers(
                    self.username,
                    self.authToken,
                    self.proxy_username,
                    self.proxy_password,
                )
            elif self.authType == "oauth":
                headers = {"Authorization": "bearer " + self.authToken}

            # set our connection for reuse
            logging.info("Network.get(): reinitializing https pool.")
            if self.proxy_address is not None and self.proxy_type is not None:
                from urllib3 import make_headers

                proxy_headers = None
                if self.proxy_username is not None and self.proxy_password is not None:
                    proxy_headers = make_headers(
                        proxy_basic_auth=self.proxy_username + ":" + self.proxy_password
                    )

                if self.proxy_type == "http":
                    self.https_pool = urllib3.ProxyManager(
                        self.proxy_address,
                        num_pools=20,
                        maxsize=self.httpsConnPoolSize,
                        timeout=self.timeout,
                        proxy_headers=proxy_headers,
                        headers=headers,
                        cert_reqs="CERT_REQUIRED",
                        ca_certs=certifi.where(),
                        retries=self.retries,
                        block=True,
                    )
            else:
                # create thread-safe pool of connections to api.thousandeyes.com
                self.https_pool = urllib3.HTTPSConnectionPool(
                    self.url,
                    port=443,
                    timeout=self.timeout,
                    headers=headers,
                    maxsize=self.httpsConnPoolSize,
                    cert_reqs="CERT_REQUIRED",
                    ca_certs=certifi.where(),
                    retries=self.retries,
                    block=True,
                )

        if type(options) is dict:
            options = urlencode(options)
        if options is not None:
            req_str = "/%s/%s.%s?%s" % (
                Network.get_api_version(),
                query,
                data_type,
                options,
            )
        else:
            req_str = "/%s/%s.%s" % (Network.get_api_version(), query, data_type)

        req = None
        throttle_ct = 0

        self.__soft_throttle()

        while True:
            try:
                req = self.https_pool.request("GET", "https://" + self.url + req_str)
            except Exception as exception:
                logging.exception("Network:get() Exception raised: %s" % exception)

            if (req is not None) and (req.status == 200):
                # Collect rate limit data from the API, so later calls can enforce soft throttling
                if "X-Organization-Rate-Limit-Limit" in req.headers:
                    self.__rate_limit = int(
                        req.headers["X-Organization-Rate-Limit-Limit"]
                    )
                    self.__rate_limit_remaining = int(
                        req.headers["X-Organization-Rate-Limit-Remaining"]
                    )
                    self.__rate_limit_reset = int(
                        req.headers["X-Organization-Rate-Limit-Reset"]
                    )

                return json.loads(req.data.decode("utf-8"))

            elif (req is not None) and (req.status == 429):
                throttle_ct += 1
                self.__throttle_rate_limit(throttle_ct, req.headers)

            else:
                if req is not None:
                    logging.warning(
                        "Network:get() :: GET request failed, HTTP status: %s request: %s"
                        % (req.status, req_str)
                    )
                else:
                    logging.warning(
                        "Network:get() :: GET request failed. No API response received."
                    )
                raise HTTPResponseError(req)

    def post(self, query, body, options=None, data_type="json"):
        """
        Purpose: performs https post request from ThousandEyes API
        Inputs:
            query: API query string
            body: POST payload, can be a string, JSON object or a dictionary
            options: HTTP options
            data_type: JSON (default), or XML (if overriden)
        Returns:
            Response or None
        """
        if self.https_pool is None:
            headers = None
            if self.authType == "basic" or self.authType is None:
                headers = self.__headers(
                    self.username,
                    self.authToken,
                    self.proxy_username,
                    self.proxy_password,
                )
            elif self.authType == "oauth":
                headers = {"Authorization": "bearer " + self.authToken}
            # set our connection for reuse
            if self.proxy_address is not None and self.proxy_type is not None:
                from urllib3 import make_headers

                proxy_headers = None
                if self.proxy_username is not None and self.proxy_password is not None:
                    proxy_headers = make_headers(
                        proxy_basic_auth=self.proxy_username + ":" + self.proxy_password
                    )

                if self.proxy_type == "http":
                    self.https_pool = urllib3.ProxyManager(
                        self.proxy_address,
                        num_pools=20,
                        maxsize=self.httpsConnPoolSize,
                        timeout=self.timeout,
                        proxy_headers=proxy_headers,
                        headers=headers,
                        cert_reqs="CERT_REQUIRED",
                        ca_certs=certifi.where(),
                        retries=self.retries,
                        block=True,
                    )
            else:
                # create thread-safe pool of connections to api.thousandeyes.com
                self.https_pool = urllib3.HTTPSConnectionPool(
                    self.url,
                    port=443,
                    timeout=self.timeout,
                    headers=headers,
                    maxsize=self.httpsConnPoolSize,
                    cert_reqs="CERT_REQUIRED",
                    ca_certs=certifi.where(),
                    retries=self.retries,
                    block=True,
                )

        if type(body) is dict:
            body = json.dumps(body)
        if type(options) is dict:
            options = urlencode(options)
        if options is not None:
            req_str = "/%s/%s.%s?%s" % (
                Network.get_api_version(),
                query,
                data_type,
                options,
            )
        else:
            req_str = "/%s/%s.%s" % (Network.get_api_version(), query, data_type)

        req = None
        throttle_ct = 0

        while True:
            try:
                req = self.https_pool.request(
                    "POST", "https://" + self.url + req_str, body=body
                )

            except Exception as exception:
                logging.exception("Network:post() Exception raised: %s" % exception)

            if (req is not None) and (req.status == 200):
                return json.loads(req.data.decode("utf-8"))
            elif (req is not None) and (req.status == 429):
                throttle_ct += 1
                self.__throttle_rate_limit(throttle_ct, req.headers)
            else:
                if req is not None:
                    logging.warning(
                        "Network:post() :: POST request failed, HTTP status: %s request: %s"
                        % (req.status, req_str)
                    )
                else:
                    logging.warning(
                        "Network:post() :: POST request failed. No API response received."
                    )
                raise HTTPResponseError(req)

    def get_apiLink(self, link, options=None, type="json"):
        """
            performs get request from ThousandEyes API using a ThousandEyes
                built-in apiLink

            Arguments:
                link: apiLink URL
                type: JSON (default), or XML (if overriden)
        """

        if self.https_pool is None:
            headers = None

            if self.authType == "basic" or self.authType is None:
                headers = self.__headers(self.username, self.authToken)
            elif self.authType == "oauth":
                headers = {"Authorization": "bearer " + self.authToken}

            # set our connection for reuse
            logging.info("Network.get(): reinitializing https pool.")
            if self.proxy_address is not None and self.proxy_type is not None:
                from urllib3 import make_headers

                proxy_headers = None
                if self.proxy_username is not None and self.proxy_password is not None:
                    proxy_headers = make_headers(
                        proxy_basic_auth=self.proxy_username + ":" + self.proxy_password
                    )

                if self.proxy_type == "http":
                    self.https_pool = urllib3.ProxyManager(
                        self.proxy_address,
                        num_pools=20,
                        maxsize=self.httpsConnPoolSize,
                        timeout=self.timeout,
                        proxy_headers=proxy_headers,
                        headers=headers,
                        cert_reqs="CERT_REQUIRED",
                        ca_certs=certifi.where(),
                        retries=self.retries,
                        block=True,
                    )
            else:
                # create thread-safe pool of connections to api.thousandeyes.com
                self.https_pool = urllib3.HTTPSConnectionPool(
                    self.url,
                    port=443,
                    timeout=self.timeout,
                    headers=headers,
                    maxsize=self.httpsConnPoolSize,
                    cert_reqs="CERT_REQUIRED",
                    ca_certs=certifi.where(),
                    retries=self.retries,
                    block=True,
                )

        url = "https://" + self.url
        path = link.replace(url, "")
        if type(options) is dict:
            options = urlencode(options)
        if options is not None:
            req_str = "%s.%s?%s" % (path, type, options)
        else:
            req_str = "%s.%s" % (path, type)

        req = None
        throttle_ct = 0
        while True:

            try:
                logging.debug("req_str: %s" % req_str)
                req = self.https_pool.request("GET", req_str)

            except Exception as exception:
                logging.exception(
                    "Network:http_get_apiLink:: EXCEPTION: %s" % exception
                )

            if (req is not None) and (req.status == 200):
                return json.loads(req.data)

            elif (req is not None) and (req.status == 429):
                throttle_ct += 1
                self.__throttle_rate_limit(throttle_ct, req.headers)

            else:
                return None

    def __get_api_url(self):
        """
        Purpose: returns api url
        Inputs:
            None
        Returns: API url
        """

        if Network.api_version is None:
            return self.url
        else:
            return "%s/%s" % (self.url, Network.api_version)

    @staticmethod
    def get_api_version():
        """
        Purpose: returns api version
        Inputs:
            None
        Returns: API version
        """

        if Network.api_version is None:
            return "v6"

        return Network.api_version

    def __resp_code(self, status_code):
        """
        Purpose: returns status code from API call
        Inputs:
            status code (integer)
        Returns: API version
        """
        switch = {
            200: "200: OK",
            201: "201: CREATED",
            204: "204: NO CONTENT",
            301: "301: MOVED PERMANENTLY",
            400: "400: BAD REQUEST",
            403: "403: FORBIDDEN",
            404: "404: NOT FOUND",
            405: "405: METHOD NOT ALLOWED",
            406: "406: NOT ACCEPTABLE",
            415: "415: UNSUPPORTED MEDIA TYPE",
            429: "429: TOO MANY REQUESTS",
            500: "500: INTERNAL SERVER ERROR",
            503: "503: SERVICE UNAVIABLE",
        }
        return switch.get(status_code, "UNKNOWN status code")

    def __headers(self, username, auth_token, proxy_username=None, proxy_password=None):
        """
        Purpose: utility to build headers for use with HTTP request basic authorization
        Inputs:
            username
            API auth token
            data_type: JSON (default), or XML (if overriden)
        """

        credentials = bytes("{}:{}".format(username, auth_token).encode("utf8"))
        encoded = base64.b64encode(credentials)

        return {
            "Authorization": "Basic %s" % encoded.decode("ascii"),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def __soft_throttle(self):
        """ This blocking method ensures API queries do not overload the API and let other applications use the API
            without interruption.

            Soft throttle delays the API query for a few seconds if the rate limit consumption is not linear, i.e.
            6 seconds into the rate limit period there should be at least 90% API calls remaining, after 30 seconds
            there should be at least 50% API calls remaining, etc. If consumption is higher, API queries are delayed.

            Soft throttle delays the API query until the next rate limit reset if the remaining API calls are under 5%
            (dynamic) of total.
        """

        while True:

            # If there are over 90% absolute calls left, go for it
            if (self.__rate_limit_remaining / self.__rate_limit) >= 0.9:
                return
            # If there are under __rate_limit_hard_keep calls left, sleep until next rate limit reset
            # Add active threads (=likely parallel calls in action) to __rate_limit_hard_keep to ensure other currently
            # running API queries are accounted for
            elif (
                self.__rate_limit_remaining
                + min(self.httpsConnPoolSize, threading.active_count())
            ) / self.__rate_limit <= self.__rate_limit_hard_keep:
                sleep_time = 1 + math.ceil(self.__rate_limit_reset - time.time())
                if sleep_time < 1:
                    sleep_time = 1
                logging.debug(
                    "Network:__soft_throttle() - soft-throttle, %d/%d API calls remaining. "
                    % (self.__rate_limit_remaining, self.__rate_limit)
                    + "Normal operations will resume in %d seconds." % sleep_time
                )
                time.sleep(sleep_time)
                return
            # Else, soft throttle to linear consumption
            soft_rate_limit_reset = self.__rate_limit_reset - (
                60 * self.__rate_limit_remaining / self.__rate_limit
            )
            if soft_rate_limit_reset < time.time():
                return

            sleep_time = math.ceil(soft_rate_limit_reset - time.time())
            if sleep_time < 1:
                sleep_time = 1
            logging.debug(
                "Network:__soft_throttle() - soft-throttle, %d/%d API calls remaining. "
                % (self.__rate_limit_remaining, self.__rate_limit)
                + "Normal operations will resume in %d seconds." % sleep_time
            )
            time.sleep(sleep_time)

    def __throttle(self, throttle_ct):
        """
        Purpose: utlity to sleep request thread
        Inputs:
            throttle count
        Returns: (no return)
        """
        # based on exponential backoff

        power = throttle_ct % 8
        sleep_time = 1.5 ** power

        logging.info(
            "Network:__exponential_throttle:: throttle_ct:%s power:%s sleep_time:%.6f"
            % (throttle_ct, power, sleep_time)
        )

        time.sleep(sleep_time)

    def __throttle_rate_limit(self, throttle_ct, resp_hdrs):
        """
        Purpose: utility to rate limit/back off
        Inputs:
            throttle count
            HTTP response headers
        Returns: (no return)
        """
        # based on response header rate limit data

        # __rate_limit_hard_keep starts at 5%, but each time 429 is hit increase it for 2%, but no more than 30%
        first = False
        if abs(self.__rate_limit_hard_keep_update - time.time()) > 10:
            self.__rate_limit_hard_keep_update = time.time()
            first = True
            self.__rate_limit_hard_keep += 0.02
            if self.__rate_limit_hard_keep > 0.3:
                self.__rate_limit_hard_keep = 0.3

        if (
            resp_hdrs["X-Organization-Rate-Limit-Limit"] is None
            or resp_hdrs["X-Organization-Rate-Limit-Remaining"] is None
            or resp_hdrs["X-Organization-Rate-Limit-Reset"] is None
        ):
            # Collect rate limit data from the API, so later calls can enforce soft throttling
            self.__rate_limit = 240
            self.__rate_limit_remaining = 0
            # we don't have the data we need, default to exponential backoff
            logging.info(
                "Network:__throttle_rate_limit:: resp_hdrs:%s missing attributes"
                % (resp_hdrs)
            )
            self.__throttle(throttle_ct)
            return

        self.__rate_limit_remaining = int(
            resp_hdrs["X-Organization-Rate-Limit-Remaining"]
        )
        self.__rate_limit_reset = int(resp_hdrs["X-Organization-Rate-Limit-Reset"])

        time_to_next_reset = int(resp_hdrs["X-Organization-Rate-Limit-Reset"]) - int(
            time.time()
        )

        if time_to_next_reset > 0:
            # need to sleep until we can get our limit reset
            # Only put it in INFO log once, the rest should go in DEBUG
            if first:
                logging.info(
                    "Network:__throttle_rate_limit() - organization API calls per limit reached. "
                    "Normal operations will resume in %s seconds. "
                    % (time_to_next_reset % 60)
                    + "Will keep %d%% calls from now on."
                    % (self.__rate_limit_hard_keep * 100)
                )
            else:
                logging.debug(
                    "Network:__throttle_rate_limit() - organization API calls per limit reached. "
                    "Normal operations will resume in %s seconds. "
                    % (time_to_next_reset % 60)
                    + "Will keep %d%% calls from now on."
                    % (self.__rate_limit_hard_keep * 100)
                )

            time.sleep(1 + time_to_next_reset % 60)


class HTTPResponseError(Exception):
    """ Raised when Network.get() or .post() methods cannot handle a HTTP Response code.

        :param response: Response object
        :type response: HTTPResponse
    """

    def __init__(self, response):
        self.status = response.status
