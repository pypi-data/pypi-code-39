"""A basic reference device emulator containing just this one tile."""

from iotile.emulate.reference import ReferenceDevice
from .accel1_1 import AccelerometerTile


class AccelerometerTileReferenceDevice(ReferenceDevice):
    """Reference implementation of an IOTile device with a single accelerometer tile.

    This device is produced as part of the firm_env component and contains a
    reference emulated device with a single accelerometer tile at address 11
    and a reference controller implementation.

    Args:
        args (dict): A dictionary of optional creation arguments.  Currently
            supported are:
                iotile_id (int or hex string): The id of this device. This
                    defaults to 1 if not specified.
    """

    STATE_NAME = "accel1_1_ref_device"
    STATE_VERSION = "0.1.0"

    def __init__(self, args):
        super(AccelerometerTileReferenceDevice, self).__init__(args)

        tile = AccelerometerTile(11, {}, self)
        self.add_tile(11, tile)
