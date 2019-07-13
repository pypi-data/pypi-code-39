# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import TYPE_CHECKING, Optional
from ..call import call, call_async, call_sync

from ..protobufs import main_pb2
from .device_identity import DeviceIdentity
from .command_code import CommandCode
from .message import Message

if TYPE_CHECKING:
    from .connection import Connection


class Device:
    """
    Represents a device using the binary protocol.
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
    def identity(self) -> Optional[DeviceIdentity]:
        """
        Identity of the device.
        """
        return self.__retrieve_identity()

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
            timeout: Number of seconds to wait for a response from the device. 0 or negative defaults to 2s.

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
            timeout: Number of seconds to wait for a response from the device. 0 or negative defaults to 2s.

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
    ) -> Optional[DeviceIdentity]:
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
        return DeviceIdentity.from_protobuf(response.identity) if response.identity is not None else None
