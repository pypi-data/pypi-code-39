from typing import Union, Any, List, Callable, Dict
from inspect import getmembers
from typing import Dict, Any
import inspect
import json
import sys
import traceback
from .config import config

try:
    from PyInquirer import prompt, Separator
except ImportError:
    raise ImportError()

try:
    from pyfiglet import figlet_format
except ImportError:
    def figlet_format(text, *args, **kwargs):
        return text

try:
    from termcolor import colored
except ImportError:
    def colored(text, *args, **kwargs):
        return text


def _invoke_method(method: Callable, args: Union[str, int, bool, Dict[str, Any]] = None) -> Any:
    if args is None:
        return method()
    if type(args) is int or type(args) is str or type(args) is bool:
        return method(args)
    return method(**args)


def _invoke_str_method(method: Union[str, Callable], cls: Any,
                       args: Union[str, int, bool, Dict[str, Any]] = None) -> Any:
    if method:
        res = str(method)
        if inspect.ismethod(method) or inspect.isfunction(method):
            try:
                res = _invoke_method(method, args)
            except Exception as e:
                return f'[Invoke of {method} failed {e}]'
        elif type(method) is str and method.startswith('self.') and cls and hasattr(cls, method[5:]):
            res = getattr(cls, method[5:])
            if inspect.ismethod(res) or inspect.isfunction(res):
                try:
                    res = _invoke_method(res, args)
                except Exception as e:
                    return f'[Invoke of {method} failed {e}]'
        if res is None:
            return res
        elif type(res) is str:
            return res if len(res) else f'[Empty string from {method}]'
        else:
            return f'[Invoked method {method} returned {type(res).__name__} instead of string]'
    return method


def banner(header: str, sub_header: str = None, spacify_header: bool = True):
    header = f' {" ".join(header)} ' if spacify_header else header
    log(header, color=config.banner_header_color, header=True, font=config.banner_figlet_font)
    if sub_header:
        log(sub_header, config.banner_subheader_color)


def log(output: str, color='blue', header: bool = False, font: str = 'block'):
    print(colored(output if not header else figlet_format(output, font=font), color))


def _add_special_choice(name: str, value: str, choices: List[Any], separate: bool = True) -> List[Any]:
    if separate:
        choices.append(Separator())
    choices.append({'name': name, 'value': value})
    return choices


def _verify_registry():
    for i in config.menu._registry:
        if config.menu._registry[i]._requires_cls and not config.menu._registry[i]._cls:
            raise ValueError(f'Method "{config.menu._registry[i]._id}" requires instance of '
                             f'"{config.menu._registry[i]._requires_cls}".'
                             f'Be sure to decorate this class using CliMenuContainer')


def shell_menu(menu_level: object):
    _verify_registry()
    scope_choices = list()
    for ch in menu_level._children:
        if not ch._disabled:
            scope_choices.append({
                'name': f'* {ch._title}' if not hasattr(ch, '_method') or not ch._method else f'~ {ch._title}',
                'value': ch._id
            })
    if menu_level._parent:
        _add_special_choice('< Back', '__back__', scope_choices)
    _add_special_choice('x Exit', '__exit__', scope_choices, False if menu_level._parent else True)
    sel = prompt({
        'type': 'list',
        'name': 'scope',
        'message': 'Chose the action' if menu_level._title == 'root' else f'Chose {menu_level._title.lower()} action:',
        'choices': scope_choices,
    }, style=config.prompt_style)
    if 'scope' not in sel or sel['scope'] == '__exit__':
        sys.exit()
    elif sel['scope'] == '__back__':
        return shell_menu(menu_level._parent)
    else:
        selection = menu_level._registry[sel['scope']]
        if not selection._method:
            shell_menu(selection)
        else:
            args_err = None
            args = {}
            if len(selection._args):
                default_args = _invoke_str_method(selection._default, cls=selection._cls)
                arg_answers = prompt(
                    {
                        'type': 'input',
                        'name': 'json', 'message': f'Enter arguments as JSON:',
                        'default': default_args
                    },
                    style=config.prompt_style)
                data = arg_answers['json'].strip() if 'json' in arg_answers else None
                if data is None:
                    return
                elif len(data):
                    try:
                        args = json.loads(data)
                    except Exception:
                        args_err = 'JSON parse error'
            if args_err:
                log(args_err, 'red')
            else:
                confirm_msg = _invoke_str_method(selection._confirm, cls=selection._cls, args=args)
            if confirm_msg:
                conf_answer = prompt(
                    {
                        'type': 'confirm',
                        'message': confirm_msg,
                        'name': 'confirm_method',
                        'default': False,
                    },
                    style=config.prompt_style)
                if 'confirm_method' not in conf_answer or not conf_answer['confirm_method']:
                    log('Canceled', 'red')
                    return
            try:
                _invoke_method(selection._method, args)
            except Exception as e:
                traceback.print_exc()
            return shell_menu(menu_level)


class CliMenu:
    _registry: Dict[str, object] = {}

    def __init__(self, title, parent: object = None):
        self._id = self._get_id(title, parent)
        self._title: str = title
        self._parent: object = parent
        self._children: List[object] = list()
        self._method: Callable = None
        self._cls: object = None
        self._requires_cls: str = None
        self._args: List[Any] = None
        self._signature: Any = None
        self._default: Union[str, Callable] = None
        self._disabled: Union[str, Callable] = None
        self._confirm: Union[str, Callable] = None
        self._registry[self._id] = self

        for n, mh in getmembers(self):
            if n not in ['title', 'parent', 'children', 'method', 'default', 'disabled',
                         'confirm', 'registry'] and not n.startswith('_') and not inspect.ismethod(mh):
                o = None
                if n[0] == n[0].capitalize():
                    if type(mh) is str:
                        o = CliMenu(n, self)
                        setattr(self, n, o)
                    elif isinstance(mh, CliMenu):
                        o = mh
                        o._parent = self
                    elif type(mh) is type:
                        raise KeyError(
                            f'Menu attribute error. Key "{n}" is a type, must be an instance of class {mh.__name__}')
                if o:
                    self._children.append(o)
        if not config.menu:
            config.menu = self

    def _append_method(self, title: str, method: Callable, default: Union[str, Callable] = None,
                       confirm: Union[str, Callable] = None, disabled: str = None,
                       args: List[Any] = None, signature: Any = None, requires_cls: str = None):
        n = CliMenu(title, self)
        n._method = method
        n._args = args
        n._signature = signature
        n._parent = self
        n._default = default
        n._confirm = confirm
        n._disabled = disabled
        n._requires_cls = requires_cls
        self._children.append(n)
        return n._id

    def _get_id(self, title: str, parent: object = None):
        pth = list([title])
        if parent is None:
            if title != 'root':
                pth.append('root')
        else:
            has_root = False
            while parent:
                pth.append(parent._title)
                if parent and parent._title == 'root':
                    has_root = True
                parent = parent._parent
            if not has_root:
                pth.append('root')
        pth.reverse()
        return '/'.join(pth)
