from typing import Union, List
from cached_property import cached_property
from pylspci.fields import hexstring, Slot, NameWithID
from pylspci.device import Device
import argparse
import shlex
import subprocess


class SimpleFormatParser(object):

    @cached_property
    def parser(self) -> argparse.ArgumentParser:
        p = argparse.ArgumentParser()
        p.add_argument(
            'slot',
            type=Slot,
        )
        p.add_argument(
            'cls',
            type=NameWithID,
        )
        p.add_argument(
            'vendor',
            type=NameWithID,
        )
        p.add_argument(
            'device',
            type=NameWithID,
        )
        p.add_argument(
            'subsystem_vendor',
            type=NameWithID,
        )
        p.add_argument(
            'subsystem_device',
            type=NameWithID,
        )
        p.add_argument(
            '-r',
            type=hexstring,
            nargs='?',
            dest='revision',
        )
        p.add_argument(
            '-p',
            type=hexstring,
            nargs='?',
            dest='progif',
        )
        return p

    def parse(self, args: Union[str, List[str]]) -> Device:
        if isinstance(args, str):
            args = shlex.split(args)
        return Device(**vars(self.parser.parse_args(args)))

    def from_lspci(self) -> List[Device]:
        return list(map(
            self.parse,
            subprocess.check_output(
                ['lspci', '-nnmm'],
                universal_newlines=True,
            ).splitlines(),
        ))
