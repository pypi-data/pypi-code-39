# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import TYPE_CHECKING
from ..call import call, call_async, call_sync

from ..protobufs import main_pb2
from .device_identity import DeviceIdentity
from .command_code import CommandCode
from .message import Message
from ..units import Units
from .device_type import DeviceType
from ..firmware_version import FirmwareVersion

if TYPE_CHECKING:
    from .connection import Connection


class Device:
    """
    Represents a device using the binary protocol.
    """

    DEFAULT_MOVEMENT_TIMEOUT = 60
    """
    Default timeout for move commands in seconds.
    """

    @property
    def connection(self) -> 'Connection':
        """
        Connection of this device.
        """
        return self._connection

    @property
    def device_address(self) -> int:
        """
        The device address uniquely identifies the device on the connection.
        It can be configured or automatically assigned by the renumber command.
        """
        return self._device_address

    @property
    def identity(self) -> DeviceIdentity:
        """
        Identity of the device.
        """
        return self.__retrieve_identity()

    @property
    def device_id(self) -> int:
        """
        Unique ID of the device hardware.
        """
        return self.identity.device_id

    @property
    def serial_number(self) -> int:
        """
        Serial number of the device.
        """
        return self.identity.serial_number

    @property
    def name(self) -> str:
        """
        Name of the product.
        """
        return self.identity.name

    @property
    def firmware_version(self) -> FirmwareVersion:
        """
        Version of the firmware.
        """
        return self.identity.firmware_version

    @property
    def is_peripheral(self) -> bool:
        """
        Indicates whether the device is a peripheral or part of an integrated device.
        """
        return self.identity.is_peripheral

    @property
    def peripheral_id(self) -> int:
        """
        Unique ID of the peripheral hardware.
        """
        return self.identity.peripheral_id

    @property
    def peripheral_name(self) -> str:
        """
        Name of the peripheral hardware.
        """
        return self.identity.peripheral_name

    @property
    def device_type(self) -> DeviceType:
        """
        Determines the type of an device and units it accepts.
        """
        return self.identity.device_type

    def __init__(self, connection: 'Connection', device_address: int):
        self._connection = connection
        self._device_address = device_address

    def generic_command(
            self,
            command: CommandCode,
            data: int = 0,
            check_errors: bool = True,
            timeout: float = 0.0
    ) -> Message:
        """
        Sends a generic Binary command to this device.
        For more information please refer to the
        [Binary Protocol Manual](https://www.zaber.com/protocol-manual?protocol=Binary#topic_quick_command_reference).

        Args:
            command: Command to send.
            data: Optional data argument to the command. Defaults to zero.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: Number of seconds to wait for a response from the device. 0 or negative defaults to 0.5s.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericBinaryRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command.value
        request.data = data
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.BinaryMessage()
        call("binary/interface/generic_command", request, response)
        return Message.from_protobuf(response)

    async def generic_command_async(
            self,
            command: CommandCode,
            data: int = 0,
            check_errors: bool = True,
            timeout: float = 0.0
    ) -> Message:
        """
        Sends a generic Binary command to this device.
        For more information please refer to the
        [Binary Protocol Manual](https://www.zaber.com/protocol-manual?protocol=Binary#topic_quick_command_reference).

        Args:
            command: Command to send.
            data: Optional data argument to the command. Defaults to zero.
            check_errors: Controls whether to throw an exception when the device rejects the command.
            timeout: Number of seconds to wait for a response from the device. 0 or negative defaults to 0.5s.

        Returns:
            A response to the command.
        """
        request = main_pb2.GenericBinaryRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command.value
        request.data = data
        request.check_errors = check_errors
        request.timeout = timeout
        response = main_pb2.BinaryMessage()
        await call_async("binary/interface/generic_command", request, response)
        return Message.from_protobuf(response)

    def generic_command_no_response(
            self,
            command: CommandCode,
            data: int = 0
    ) -> None:
        """
        Sends a generic Binary command to this device without expecting a response.
        For more information please refer to the
        [Binary Protocol Manual](https://www.zaber.com/protocol-manual?protocol=Binary#topic_quick_command_reference).

        Args:
            command: Command to send.
            data: Optional data argument to the command. Defaults to zero.
        """
        request = main_pb2.GenericBinaryRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command.value
        request.data = data
        call("binary/interface/generic_command_no_response", request)

    async def generic_command_no_response_async(
            self,
            command: CommandCode,
            data: int = 0
    ) -> None:
        """
        Sends a generic Binary command to this device without expecting a response.
        For more information please refer to the
        [Binary Protocol Manual](https://www.zaber.com/protocol-manual?protocol=Binary#topic_quick_command_reference).

        Args:
            command: Command to send.
            data: Optional data argument to the command. Defaults to zero.
        """
        request = main_pb2.GenericBinaryRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.command = command.value
        request.data = data
        await call_async("binary/interface/generic_command_no_response", request)

    def home(
            self,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Homes device. Device returns to its homing position.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceHomeRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        call("binary/device/home", request)

    async def home_async(
            self,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Homes device. Device returns to its homing position.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceHomeRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        await call_async("binary/device/home", request)

    def stop(
            self,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Stops ongoing device movement. Decelerates until zero speed.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceStopRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        call("binary/device/stop", request)

    async def stop_async(
            self,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Stops ongoing device movement. Decelerates until zero speed.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceStopRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        await call_async("binary/device/stop", request)

    def move_absolute(
            self,
            position: float,
            unit: Units = Units.Native,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Move device to absolute position.

        Args:
            position: Absolute position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.ABS
        request.arg = position
        request.unit = unit.value
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        call("binary/device/move", request)

    async def move_absolute_async(
            self,
            position: float,
            unit: Units = Units.Native,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Move device to absolute position.

        Args:
            position: Absolute position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.ABS
        request.arg = position
        request.unit = unit.value
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        await call_async("binary/device/move", request)

    def move_relative(
            self,
            position: float,
            unit: Units = Units.Native,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Move device to position relative to current position.

        Args:
            position: Relative position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.REL
        request.arg = position
        request.unit = unit.value
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        call("binary/device/move", request)

    async def move_relative_async(
            self,
            position: float,
            unit: Units = Units.Native,
            wait_until_idle: bool = True,
            timeout: float = DEFAULT_MOVEMENT_TIMEOUT
    ) -> None:
        """
        Move device to position relative to current position.

        Args:
            position: Relative position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
                If set to false, errors during movement may not be detected.
            timeout: Number of seconds to wait for response from the device chain (defaults to 60s).
                Only use when waitUntilIdle = true.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.REL
        request.arg = position
        request.unit = unit.value
        request.wait_until_idle = wait_until_idle
        request.timeout = timeout
        await call_async("binary/device/move", request)

    def move_velocity(
            self,
            velocity: float,
            unit: Units = Units.Native
    ) -> None:
        """
        Begins to move device at specified speed.

        Args:
            velocity: Movement velocity.
            unit: Units of velocity.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.VEL
        request.wait_until_idle = True
        request.arg = velocity
        request.unit = unit.value
        call("binary/device/move", request)

    async def move_velocity_async(
            self,
            velocity: float,
            unit: Units = Units.Native
    ) -> None:
        """
        Begins to move device at specified speed.

        Args:
            velocity: Movement velocity.
            unit: Units of velocity.
        """
        request = main_pb2.BinaryDeviceMoveRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        request.type = main_pb2.BinaryDeviceMoveRequest.VEL
        request.wait_until_idle = True
        request.arg = velocity
        request.unit = unit.value
        await call_async("binary/device/move", request)

    def wait_until_idle(
            self
    ) -> None:
        """
        Waits until device stops moving.
        """
        request = main_pb2.BinaryDeviceWaitUntilIdleRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        call("binary/device/wait_until_idle", request)

    async def wait_until_idle_async(
            self
    ) -> None:
        """
        Waits until device stops moving.
        """
        request = main_pb2.BinaryDeviceWaitUntilIdleRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        await call_async("binary/device/wait_until_idle", request)

    def identify(
            self
    ) -> DeviceIdentity:
        """
        Queries the device and the database, gathering information about the product.
        Without this information features such as unit conversions will not work.
        Usually, called automatically by detect devices method.

        Returns:
            Device identification data.
        """
        request = main_pb2.BinaryDeviceIdentifyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.BinaryDeviceIdentity()
        call("binary/device/identify", request, response)
        return DeviceIdentity.from_protobuf(response)

    async def identify_async(
            self
    ) -> DeviceIdentity:
        """
        Queries the device and the database, gathering information about the product.
        Without this information features such as unit conversions will not work.
        Usually, called automatically by detect devices method.

        Returns:
            Device identification data.
        """
        request = main_pb2.BinaryDeviceIdentifyRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.BinaryDeviceIdentity()
        await call_async("binary/device/identify", request, response)
        return DeviceIdentity.from_protobuf(response)

    def __repr__(
            self
    ) -> str:
        """
        Returns a string that represents the device.

        Returns:
            A string that represents the device.
        """
        request = main_pb2.ToStringRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.ToStringResponse()
        call_sync("binary/device/device_to_string", request, response)
        return response.to_str

    def __retrieve_identity(
            self
    ) -> DeviceIdentity:
        """
        Returns identity.

        Returns:
            Device identity.
        """
        request = main_pb2.BinaryDeviceGetIdentityRequest()
        request.interface_id = self.connection.interface_id
        request.device = self.device_address
        response = main_pb2.BinaryDeviceGetIdentityResponse()
        call_sync("binary/device/get_identity", request, response)
        return DeviceIdentity.from_protobuf(response.identity)
