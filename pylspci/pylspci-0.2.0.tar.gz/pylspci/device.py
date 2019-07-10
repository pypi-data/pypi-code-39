from typing import NamedTuple, Optional, List
from pylspci.fields import Slot, NameWithID


class Device(NamedTuple):
    """
    Describes a device returned by lspci.
    """

    slot: Slot
    """
    The device's slot (domain, bus, number and function).

    :type: Slot
    """

    cls: NameWithID
    """
    The device's class, with a name and/or an ID.

    :type: NameWithID
    """

    vendor: NameWithID
    """
    The device's vendor, with a name and/or an ID.

    :type: NameWithID
    """

    device: NameWithID
    """
    The device's name and/or ID.

    :type: NameWithID
    """

    subsystem_vendor: Optional[NameWithID] = None
    """
    The device's subsystem vendor, if found, with a name and/or an ID.

    :type: NameWithID or None
    """

    subsystem_device: Optional[NameWithID] = None
    """
    The device's subsystem name and/or ID, if found.

    :type: NameWithID or None
    """

    revision: Optional[int] = None
    """
    The device's revision number.

    :type: int or None
    """

    progif: Optional[int] = None
    """
    The device's programming interface number.

    :type: int or None
    """

    driver: Optional[str] = None
    """
    The device's driver (Linux only).

    :type: str or None
    """

    kernel_modules: List[str] = []
    """
    One or more kernel modules that can handle this device (Linux only).

    :type: List[str] or None
    """
