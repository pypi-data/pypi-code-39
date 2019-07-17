from typing import Callable, Dict, Any, Tuple, Union, List

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask_restful import Resource
from werkzeug.datastructures import ImmutableMultiDict

try:
    from utils.file import File
    from service.authentication import AuthenticationFactory
    from controller.request import Request
    from errors import IncomingDataValueError
    from utils.package import Package
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.utils.file import File
    from pysubway.service.authentication import AuthenticationFactory
    from pysubway.controller.request import Request
    from pysubway.errors import IncomingDataValueError
    from pysubway.utils.package import Package

__all__ = [
    'ViewRestful', 'View'
]


class View:

    @staticmethod
    def new_app_this_dir(dirname: str) -> Flask:
        """

        :param dirname: example File.this_dir(__file__)}/templates
        :return:
        """
        return Flask(__name__, template_folder=dirname)

    @staticmethod
    def resp_template(template: str = 'index.html', **kwargs: Any) -> str:
        """
        view function
        :return index.html
        """
        return render_template(template, **kwargs)

    @staticmethod
    def resp_file(sent_file: str) -> str:
        """
        view function
        :param sent_file: the file will be sent.
        :param authenticate: authenticate account and password
        :return:
        """
        return send_file(sent_file)

    @staticmethod
    def set_template_folder(full_path_dirname: str = '') -> str:
        """
        declare template_folder
        :param full_path_dirname: 
        :return: 
        """
        if full_path_dirname:
            return full_path_dirname
        dirname: str = full_path_dirname or File.this_dir(__file__)
        return File.join_path(dirname, 'templates')

    @staticmethod
    def authenticate(style: str = 'file', **kwargs: Any) -> Callable[[str, str], bool]:
        """
        warp AuthenticationFactory
        :param style: call AuthenticationFile
        :param kwargs: called class construction method params
        :return: callable object, params are (account, password) and returned value is bool
        """
        return AuthenticationFactory(style)(**kwargs).is_authenticated

    @classmethod
    def register_router(cls, app: Flask, router: Dict[Tuple[str, Callable], Dict]) -> None:
        """

        :param app:
        :param router: key is a Tuple: url and view function; value is other options
        :return:
        """
        for basic, options in router.items():
            url, view_func = basic
            app.add_url_rule(url, view_func=view_func, **options)

    @staticmethod
    def request_form(*keys: str) -> Union[ImmutableMultiDict, List[Any]]:
        """
        front end config:
        action: request url
        name: name is necessary, name is ImmutableMultiDict item key
        example:
        <form role="form" action="/download-file/"
                  target="_self"
                  accept-charset="UTF-8"
                  method="POST"
                  autocomplete="off"
                  enctype="application/x-www-form-urlencoded">

            <textarea name="biz_data"></textarea>
            <input ..../>
        </form>
        :return:
        """
        return [request.form.get(key) for key in keys] if keys else request.form


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
