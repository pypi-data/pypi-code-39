import requests
from flask import Response

from .views import View
from ..utils.logs import Log
from ..auth.backends import get_auth_module, get_topic

class AuthBackend:

    def authenticate(self, *args, **kwargs):
        """

        :param request:
        :return:
        """

        try:

            AuthBackend = get_auth_module()
            is_valid = AuthBackend().authenticate(*args, **kwargs)
            if is_valid:
                return True, requests.codes.ok

        except TypeError as e:
            return e, requests.codes.server_error

        except Exception as e:
            return e, requests.codes.unauthorized
