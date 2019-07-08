__all__ = ["StopParsing", "ControlAction", "Yaap"]

import sys
import json
import yaml
import argparse
from dataclasses import dataclass, field
from typing import Dict, Sequence

import jsonschema

from .argument import *


class StopParsing(Exception):

    def __init__(self, args: Sequence[str]):
        super(StopParsing, self).__init__()
        self.args = args


class ControlAction(argparse.Action):

    def __init__(self, *args, arse=None, **kwargs):
        super(ControlAction, self).__init__(*args, **kwargs)
        self.arse: Yaap = arse

        assert self.arse is not None
        subparser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
        group = subparser.add_mutually_exclusive_group()
        group.add_argument("--load", type=str, metavar="CONFIG")
        group.add_argument("--schema", action="store_true", default=False)
        self.subparser = subparser

    def show_schema(self):
        schema = self.arse.schema()
        sys.stdout.write(json.dumps(schema, ensure_ascii=False, indent=2))
        sys.exit()

    def __call__(self, parser, namespace, values, option_string=None):
        delattr(namespace, self.dest)
        if not values:
            return
        values = ["--" + v.lstrip(self.arse.control_char)
                  if v.startswith(self.arse.control_char) else v for v in
                  values]
        subargs = self.subparser.parse_args(values)
        if subargs.schema:
            self.show_schema()
        elif subargs.load is not None:
            with open(subargs.load, "r") as f:
                cfg = yaml.safe_load(f)
            self.arse.validate(cfg)
            args = []
            for k, v in cfg.items():
                if v is None:
                    continue
                arg: Argument = self.arse.arguments[k]
                if isinstance(v, bool):
                    assert isinstance(arg, Bool)
                    if v != arg.invert:
                        args.append(f"--{k}")
                elif isinstance(v, str):
                    args.extend([f"--{k}", v])
                elif isinstance(v, list):
                    args.append(f"--{k}")
                    args.extend(map(str, v))
                else:
                    args.extend((f"--{k}", str(v)))
            raise StopParsing(args)


@dataclass
class Yaap:
    name: str = None
    desc: str = None
    control_char: str = "@"
    parser: argparse.ArgumentParser = field(init=False, hash=False)
    arguments: Dict[str, Argument] = field(init=False, hash=False,
                                           default_factory=dict)

    def __post_init__(self):
        if len(self.control_char) > 1:
            raise ValueError(f"control character must not be a string: "
                             f"len({self.control_char}) > 1")
        self.parser = argparse.ArgumentParser(
            prog=None if self.name is None else self.name,
            description=None if self.desc is None else self.desc,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        self.parser.add_argument("CONTROL", nargs="*",
                                 action=lambda *args, **kwargs:
                                 ControlAction(*args, arse=self, **kwargs))

    def add(self, arg: Argument):
        if arg.name in self.arguments:
            raise IndexError(f"argument of the same name exists: "
                             f"{self.arguments[arg.name]}")
        self.arguments[arg.name] = arg
        args, kwargs = arg.generate_args()
        self.parser.add_argument(*args, **kwargs)

    def add_int(self, *args, **kwargs):
        return self.add(Int(*args, **kwargs))

    def add_float(self, *args, **kwargs):
        return self.add(Float(*args, **kwargs))

    def add_path(self, *args, **kwargs):
        return self.add(Path(*args, **kwargs))

    def add_str(self, *args, **kwargs):
        return self.add(Str(*args, **kwargs))

    def add_intlist(self, *args, **kwargs):
        return self.add(IntList(*args, **kwargs))

    def add_floatlist(self, *args, **kwargs):
        return self.add(FloatList(*args, **kwargs))

    def add_pathlist(self, *args, **kwargs):
        return self.add(PathList(*args, **kwargs))

    def add_strlist(self, *args, **kwargs):
        return self.add(StrList(*args, **kwargs))

    def add_bool(self, *args, **kwargs):
        return self.add(Bool(*args, **kwargs))

    def schema(self) -> dict:
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": str(hash((self.name, self.desc))),
            "type": "object",
            "properties": {arg.name: arg.json_schema()
                           for arg in self.arguments.values()},
            "required": [arg.name for arg in
                         self.arguments.values() if arg.required]
        }

    def validate(self, args: dict):
        jsonschema.validate(args, self.schema())

    def parse(self, args: Sequence[str] = None) -> dict:
        try:
            args = self.parser.parse_args(args)
        except StopParsing as e:
            args = self.parser.parse_args(e.args)
        return vars(args)
