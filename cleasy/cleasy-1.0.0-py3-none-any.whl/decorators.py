from typing import Any, Union, Callable
import inspect
from .shell import CliMenu
from .config import config


def _is_cli_decorator(o: Any):
    try:
        return hasattr(o, "cli_decorator")
    except:
        pass
    return False


def _cli_handler(name: str, path: CliMenu = None, default: Union[str, int, bool, Callable] = None,
                 confirm: Union[str, Callable] = None,
                 disabled: str = None):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            f(*args, **kwargs)

        menu_container = path if path else config.menu
        sig = inspect.signature(f)

        if not isinstance(menu_container, CliMenu):
            raise KeyError(f'Cli menu key "{path}"<{type(path).__name__}> used in decorator for "{name}", '
                           f'must be an instance of {CliMenu.__name__}')

        setattr(wrapped_f, 'cli_decorator', menu_container._append_method(
            title=name,
            method=wrapped_f,
            default=str(default) if default is not None else None,
            confirm=confirm,
            disabled=disabled,
            args=[a for a in inspect.getfullargspec(f).args if a != 'self'],
            signature=sig if sig.parameters else None,
            requires_cls=None if f.__module__ == '__main__' else f.__module__))
        return wrapped_f

    return wrap


CliMenuItem = _cli_handler


class CliMenuContainer(object):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, cls, *args, **kwargs):
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                for n, mh in inspect.getmembers(self):
                    if _is_cli_decorator(mh):
                        config.menu._registry[mh.cli_decorator]._method = mh
                        config.menu._registry[mh.cli_decorator]._cls = self

        return Wrapped
