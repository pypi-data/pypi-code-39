from typing import Union, List
from cached_property import cached_property
from pylspci.parsers.base import Parser
from pylspci.fields import hexstring, Slot, NameWithID
from pylspci.device import Device
import argparse
import shlex


class SimpleParser(Parser):
    """
    A parser for lspci -mm.
    """

    @cached_property
    def _parser(self) -> argparse.ArgumentParser:
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

    def parse(self, data: Union[str, List[str]]) -> List[Device]:
        """
        Parse a multiline string or a list of single-line strings
        from lspci -mm into devices.

        :param data: String or list of strings to parse from.
        :type data: str or List[str]
        :return: A list of parsed devices.
        :rtype: List[Device]
        """
        if isinstance(data, str):
            data = data.splitlines()
        return list(map(self.parse_line, data))

    def parse_line(self, args: Union[str, List[str]]) -> Device:
        """
        Parse a single line from lspci -mm into a single device, either
        as the line or as a list of fields.

        :param args: Line or list of fields to parse from.
        :type args: str or List[str]
        :return: A single parsed device.
        :rtype: Device
        """
        if isinstance(args, str):
            args = shlex.split(args)
        return Device(**vars(self._parser.parse_args(args)))
