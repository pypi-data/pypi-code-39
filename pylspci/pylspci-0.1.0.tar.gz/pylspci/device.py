from typing import NamedTuple, Optional
from pylspci.fields import Slot, NameWithID


class Device(NamedTuple):
    slot: Slot
    cls: NameWithID
    vendor: NameWithID
    device: NameWithID
    subsystem_vendor: Optional[NameWithID]
    subsystem_device: Optional[NameWithID]
    revision: Optional[int]
    progif: Optional[int]
