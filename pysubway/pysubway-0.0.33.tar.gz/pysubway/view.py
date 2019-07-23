from typing import Dict, Any

import flask
from flask_restful import Resource

try:
    from errors import AuthenticationFailed
    from errors import IncomingDataValueError
    from request import Request
    from response import Response
    from service.authentication import AuthenticationFactory
    from utils.package import Package
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.errors import AuthenticationFailed
    from pysubway.errors import IncomingDataValueError
    from pysubway.request import Request
    from pysubway.response import Response
    from pysubway.service.authentication import AuthenticationFactory
    from pysubway.utils.package import Package

__all__ = [
    'ViewRestful', 'View'
]


class View:
    request: Request = Request()
    response = Response()

    @classmethod
    def login(cls, key_username: str,
              key_password: str,
              response_data: Response,
              is_aborted: bool = True,
              prompt: str = 'account or password is wrong',
              style: str = 'file',
              **kwargs: str) -> flask.Response:
        """
        login method.

        :param key_username: username key of the incoming data
        :param key_password: username password of the incoming data
        :param response_data: if authenticated successfully, response data.
        :param is_aborted: if not abort, raise  AuthenticationFailed exception.
        :param style: authentication style, default file
        :param prompt: if authenticated failed, the prompt information.
        :param kwargs:
            about the kwargs,please refer to AuthenticationFactory
            if authentication style is file, kwargs is:
                code_book=f'{File.this_dir(__file__)}/static/code_book.ini', section='huizumodel'
        :return:
        """
        account, password = cls.request.get_data(key_username, key_password)
        is_authenticated = AuthenticationFactory(style)(**kwargs).is_authenticated(account, password)
        if not is_authenticated:
            return cls.response.handle_exception(AuthenticationFailed(prompt), is_aborted, 401)
        return response_data


class ViewRestful(Resource):
    request: Request = Request()
    service: Dict = dict()

    @classmethod
    def set_service(cls, package_path: str, prefix: str) -> Dict[str, Any]:
        return Package(package_path).get_classes(prefix)

    def exec_service(self) -> Dict[str, Any]:
        if not self.service:
            pass
        cls_name, method_name, _ = self.request.service
        exec_method = getattr(self.service.get(cls_name), method_name)
        if not exec_method:
            raise IncomingDataValueError(f'class cls_name {cls_name} do not have method {method_name}')
        return exec_method(self.request.data)

    def get(self) -> str:
        return 'hello pysubway ...'
