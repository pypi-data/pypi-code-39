import sys
import argparse
import typing
from inspect import signature, getdoc
from mangum.__version__ import __version__


class CLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=f"Mangum CLI {__version__}")
        self.subparsers = self.parser.add_subparsers()

    def __call__(self, name: str = None) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            parser_name = name or func.__name__
            parser = self.subparsers.add_parser(parser_name, help=getdoc(func))
            sig = signature(func)
            parser.set_defaults(func=func)
            kwargs = {}
            for parameter in sig.parameters.values():
                if parameter.annotation is not parameter.empty:
                    kwargs["type"] = parameter.annotation
                if parameter.default is not parameter.empty:
                    arg_name = f"--{parameter.name}"
                    kwargs["default"] = parameter.default
                else:
                    arg_name = parameter.name
                parser.add_argument(arg_name, **kwargs)
            return func

        return decorator

    def cli(self, args=None):
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit()
        args = self.parser.parse_args()
        _args = vars(args)
        func = _args.pop("func")
        func(**_args)
