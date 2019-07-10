from typing import Union, List, NamedTuple, Callable, Any
from pylspci.parsers.base import Parser
from pylspci.device import Device
from pylspci.fields import hexstring, Slot, NameWithID


class FieldMapping(NamedTuple):
    """
    Helper class to map verbose output field names such as ``SVendor`` to
    :class:`Device` fields such as ``subsytem_vendor``.
    """

    field_name: str
    """
    Field name on the :class:`Device` named tuple.

    :type: str
    """

    field_type: Callable[[str], Any]
    """
    Field type; a callable to use to parse the string value.

    :type: Callable[[str], Any]
    """

    many: bool = False
    """
    Whether or not to use a List, if this field can be repeated multiple times
    in the lspci output.

    :type: bool
    """


class VerboseParser(Parser):
    """
    A parser for lspci -vvvmmk
    """

    default_lspci_args = {
        'verbose': True,
        'kernel_drivers': True,
    }

    # Maps lspci output fields to Device fields with a type
    _field_mapping = {
        'Slot': FieldMapping(field_name='slot', field_type=Slot),
        'Class': FieldMapping(field_name='cls', field_type=NameWithID),
        'Vendor': FieldMapping(field_name='vendor', field_type=NameWithID),
        'Device': FieldMapping(field_name='device', field_type=NameWithID),
        'SVendor': FieldMapping(
            field_name='subsystem_vendor',
            field_type=NameWithID,
        ),
        'SDevice': FieldMapping(
            field_name='subsystem_device',
            field_type=NameWithID,
        ),
        'Rev': FieldMapping(field_name='revision', field_type=hexstring),
        'ProgIf': FieldMapping(field_name='progif', field_type=hexstring),
        'Driver': FieldMapping(field_name='driver', field_type=str),
        'Module': FieldMapping(
            field_name='kernel_modules',
            field_type=str,
            many=True,
        ),
    }

    def _parse_device(self, device_data: Union[str, List[str]]) -> Device:
        devdict = {}
        if isinstance(device_data, str):
            device_data = device_data.splitlines()

        for line in device_data:
            key, _, value = map(str.strip, line.partition(':'))
            assert key in self._field_mapping, \
                'Unsupported key {!r}'.format(key)
            field = self._field_mapping[key]
            if field.many:
                devdict.setdefault(field.field_name, []) \
                       .append(field.field_type(value))
            else:
                devdict[field.field_name] = field.field_type(value)

        return Device(**devdict)

    def parse(self, data: Union[str, List[str]]) -> List[Device]:
        """
        Parse an lspci -vvvmm[nnk] output, either as a single string holding
        multiple devices separated by two newlines,
        or as a list of multiline strings holding one device each.

        :param data: One string holding a full lspci output,
           or multiple strings holding one device each.
        :type data: str or List[str]
        :return: A list of parsed devices.
        :rtype: List[Device]
        """
        if isinstance(data, str):
            data = data.split('\n\n')
        return list(map(
            self._parse_device,
            filter(bool, map(str.strip, data)),  # Ignore empty strings
        ))
