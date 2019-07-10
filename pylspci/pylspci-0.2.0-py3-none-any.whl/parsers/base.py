from abc import ABC, abstractmethod
from typing import Union, List, Mapping, Any
from pylspci.device import Device
from pylspci.command import lspci


class Parser(ABC):

    default_lspci_args: Mapping[str, Any] = {}
    """
    The default arguments that, when sent to :func:`lspci`, should provide the
    best output for this parser.

    See :func:`lspci`'s documentation for a list of available arguments.
    """

    @abstractmethod
    def parse(self, data: Union[str, List[str]]) -> List[Device]:
        """
        Parse a string or list of strings as a list of devices.

        :param data: A string holding multiple devices
           or a list of strings, one for each device.
        :type data: str or List[str]
        :returns: A list of parsed devices.
        :rtype: List[Device]
        """

    def run(self, **kwargs: Mapping[str, Any]) -> List[Device]:
        """
        Run the lspci command with the given arguments, defaulting to the
        parser's default arguments, and parse the result.

        :param **kwargs: Optional arguments to override the parser's default
           arguments. See :func:`lspci`'s documentation for a list of
           available arguments.
        :type **kwargs: Mapping[str, Any]
        :returns: A list of parsed devices.
        :rtype: List[Device]
        """
        lspci_kwargs = self.default_lspci_args.copy()
        lspci_kwargs.update(kwargs)
        return self.parse(lspci(**lspci_kwargs))
