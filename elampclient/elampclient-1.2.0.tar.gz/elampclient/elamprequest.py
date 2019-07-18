import requests
import json
import six
import random
import time
import sys
import platform
from .version import __version__

import logging
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

_TOO_MANY_REQUESTS = 429


class eLampRequest(object):
    def __init__(self, proxies=None):

        client_name = __name__.split('.')[0]
        client_version = __version__  # Version is returned from version.py

        # Construct the user-agent header with the package info, Python version and OS version.
        self.default_user_agent = {
            "client": "{0}/{1}".format(client_name, client_version),
            "python": "Python/{v.major}.{v.minor}.{v.micro}".format(v=sys.version_info),
            "system": "{0}/{1}".format(platform.system(), platform.release())
        }

        self.custom_user_agent = None
        self.proxies = proxies

    def get_user_agent(self):
        # Check for custom user-agent and append if found
        if self.custom_user_agent:
            custom_ua_list = ["/".join(client_info) for client_info in self.custom_user_agent]
            custom_ua_string = " ".join(custom_ua_list)
            self.default_user_agent['custom'] = custom_ua_string

        # Concatenate and format the user-agent string to be passed into request headers
        ua_string = []
        for key, val in self.default_user_agent.items():
            ua_string.append(val)

        user_agent_string = " ".join(ua_string)
        return user_agent_string

    def append_user_agent(self, name, version):
        if self.custom_user_agent:
            self.custom_user_agent.append([name.replace("/", ":"), version.replace("/", ":")])
        else:
            self.custom_user_agent = [[name, version]]

    def is_json_data(self, data):
        try:
            json_object = json.loads(data)
        except ValueError:
            return False
        return True

    def _should_retry_response(self, resp):
        if not resp:
            return True

        # Retry on 5xx errors.
        if resp.status_code >= 500:
            return True

        # Retry on 429 errors.
        if resp.status_code == _TOO_MANY_REQUESTS:
            return True

        # Everything inside 200-299 status code is OK => should not be retried
        if resp.status_code >= 200 and resp.status_code < 300:
            return False

        if resp.status_code >= 300:
            return True

    def do(self, token, request="?", http_method='post', post_data=None, domain="api.elamp.fr", timeout=None, retries=3):
        """
        Perform a POST request to the eLamp Web API
        Args:
            token (str): your authentication token
            request (str): the method to call from the eLamp API.
            timeout (float): stop waiting for a response after a given number of seconds
            post_data (dict): key/value arguments to pass for the request.
            domain (str): if for some reason you want to send your request to something other
                than api.elamp.fr
        """

        url = 'https://{0}/{1}'.format(domain, request)

        # Override token header if `token` is passed in post_data
        if post_data is not None and "token" in post_data:
            token = post_data['token']

        # Set user-agent and auth headers
        headers = {
            'user-agent': self.get_user_agent(),
            'Authorization': 'Bearer {}'.format(token)
        }

        post_data = post_data or {}

        if isinstance(post_data, str) and self.is_json_data(post_data):
            headers['Content-Type'] = 'application/json'
        elif isinstance(post_data, (list, dict)):
            try:
                post_data = json.dumps(post_data)
                headers['Content-Type'] = 'application/json'
            except ValueError:
                pass


        # Convert any params which are list-like to JSON strings
        # Example: `attachments` is a dict, and needs to be passed as JSON
        # for k, v in six.iteritems(post_data):
        #    if isinstance(v, (list, dict)):
        #        post_data[k] = json.dumps(v)

        # Submit the request
        resp = None
        for retry_num in range(retries + 1):
            if retry_num > 0:
                sleep_time = random.random() * 2 ** retry_num
                logger.info('[elamp] request : retrying request, attempt {} after {} seconds'.format(retry_num, sleep_time))
                time.sleep(sleep_time)
            logger.info('[elamp] request : [{}] {}'.format(http_method, url))
            exception = None
            try:
                resp = requests.request(
                    http_method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=timeout,
                    proxies=self.proxies
                )
            except Exception as e:
                exception = e

            if exception:
                if retry_num == retries:
                    raise exception
                else:
                    continue

            if not self._should_retry_response(resp):
                break

        return resp
