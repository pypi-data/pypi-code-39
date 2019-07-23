from typing import Any
from typing import Dict, Tuple, Callable

from flask import Flask
from flask_restful import Api

__all__ = [
    'Router',
]


class Router:

    @staticmethod
    def urljoin(front: str, *url: str) -> str:
        base = front if front.startswith('/') else '/{}'.format(front)
        join = ''.join((base, *[i[1:] if i.startswith('/') else i for i in url]))
        return join if join.endswith('/') else join + '/'

    @classmethod
    def bind(cls, api: Api, first_urls: Dict[str, Any], *args: Dict[str, Any]) -> None:
        u = first_urls.copy()
        for i in args:
            u.update(i)
        for url, classs in u.items():
            print('[Router] bind', url, classs.__name__)
            api.add_resource(classs, url)

    @classmethod
    def export(cls, urls: Dict[str, Any], url_prefix: str = '') -> Dict[str, Any]:
        return {cls.urljoin(url_prefix, k): v for k, v in urls.items()}

    @classmethod
    def register(cls, app: Flask, router: Dict[Tuple[str, Callable], Dict]) -> None:
        """
        :param app:
        :param router: key is a Tuple: url and view function; value is other options
        :return:
        """
        for basic, options in router.items():
            url, view_func = basic
            app.add_url_rule(url, view_func=view_func, **options)
