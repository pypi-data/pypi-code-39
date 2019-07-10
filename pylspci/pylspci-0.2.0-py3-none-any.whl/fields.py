from functools import partial
from typing import Optional
import re


hexstring = partial(int, base=16)


class Slot(object):
    """
    Describes a PCI slot identifier, in the format ``[DDDD:]BB:dd.f``,
    where ``D`` is the domain, ``B`` the bus, ``d`` the device
    and ``f`` the function. The first three are hexadecimal numbers, but
    ``f`` is in octal.
    """

    domain: int = 0x0000
    """
    The slot's domain, as a four-digit hexadecimal number.
    When omitted, defaults to ``0x0000``.

    :type: int
    """

    bus: int
    """
    The slot's bus, as a two-digit hexadecimal number.

    :type: int
    """

    device: int
    """
    The slot's device, as a two-digit hexadecimal number.

    :type: int
    """

    function: int
    """
    The slot's function, as a single octal digit.

    :type: int
    """

    def __init__(self, value: str) -> None:
        data = list(map(hexstring, re.split(r'[:\.]', value)))
        if len(data) == 3:
            data.insert(0, 0)
        self.domain, self.bus, self.device, self.function = data

    def __str__(self) -> str:
        return '{:04x}:{:02x}:{:02x}.{:01x}'.format(
            self.domain, self.bus, self.device, self.function,
        )

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__, str(self))


class NameWithID(object):
    """
    Describes a device, vendor or class with either
    a name, an hexadecimal PCI ID, or both.
    """

    id: Optional[int]
    """
    The PCI ID as a four-digit hexadecimal number.

    :type: int or None
    """

    name: Optional[str]
    """
    The human-readable name associated with this ID.

    :type: str or None
    """

    _NAME_ID_REGEX = re.compile(r'^(?P<name>.+)\s\[(?P<id>[0-9a-fA-F]{4})\]$')

    def __init__(self, value: Optional[str]) -> None:
        if value and value.endswith(']'):
            # Holds both an ID and a name
            gd = self._NAME_ID_REGEX.match(value).groupdict()
            self.id = hexstring(gd['id'])
            self.name = gd['name']
            return

        try:
            self.id = hexstring(value)
            self.name = None
        except (TypeError, ValueError):
            self.id = None
            self.name = value

    def __str__(self) -> str:
        if self.id and self.name:
            return '{} [{:04x}]'.format(self.name, self.id)
        elif self.name:
            return self.name
        elif self.id:
            return '{:04x}'.format(self.id)
        else:
            return ''

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__, str(self))
