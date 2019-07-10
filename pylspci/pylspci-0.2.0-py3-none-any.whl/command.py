from enum import Enum
from typing import Optional, Union, List, Mapping, Any
from pathlib import Path
import subprocess

OptionalPath = Optional[Union[str, Path]]


class IDResolveOption(Enum):
    """
    ``lspci`` device, vendor, class names outputting options.
    """

    NameOnly = ''
    """
    Only output the names.
    """

    IDOnly = '-n'
    """
    Only output the hexadecimal IDs.
    This is the only option that does not require a ``pciids`` file.
    """

    Both = '-nn'
    """
    Output both the names and hexadecimal IDs, in the format ``Name [ID]``.
    """


def lspci(
        pciids: OptionalPath = None,
        pcimap: OptionalPath = None,
        access_method: Optional[str] = None,
        pcilib_params: Mapping[str, Any] = {},
        file: OptionalPath = None,
        verbose: bool = False,
        kernel_drivers: bool = False,
        hide_single_domain: bool = True,
        id_resolve_option: IDResolveOption = IDResolveOption.Both,
        ) -> str:
    """
    Call the ``lspci`` command with various parameters.

    :param pciids: An optional path to a ``pciids`` file,
       to convert hexadecimal class, vendor or device IDs into names.
    :type pciids: str or Path or None
    :param pcimap: An optional path to a ``pcimap`` file,
       linking Linux kernel modules and their supported PCI IDs.
    :type pcimap: str or Path or None
    :param access_method: The access method to use to find devices.
       Set this to ``help`` to list the available access methods.
    :type access_method: str or None
    :param file: An hexadecimal dump from ``lspci -x`` to load data from,
       instead of accessing real hardware.
    :type file: str or Path or None
    :param bool verbose: Increase verbosity.
       This radically changes the output format.
    :param bool kernel_drivers: Also include kernel modules and drivers
       in the output. Only has effect with the verbose output.
    :param bool hide_single_domain: If there is a single PCI domain on this
       machine and it is numbered ``0000``, hide it from the slot numbers.
    :param id_resolve_option: Device, vendor or class ID outputting mode.
       See the :class:`IDResolveOption` docs for more details.
    :type id_resolve_option: IDResolveOption
    :return: Any output from the ``lspci`` command.
    :rtype: str
    :raises subprocess.CalledProcessError:
       ``lspci`` returned a non-zero error code.
    """
    args: List[str] = ['lspci', '-mm']
    if verbose:
        args.append('-vvv')
    if kernel_drivers:
        args.append('-k')
    if not hide_single_domain:
        args.append('-D')
    if access_method:
        args.append('-A{}'.format(access_method))
    if id_resolve_option != IDResolveOption.NameOnly:
        args.append(id_resolve_option.value)

    if pciids:
        args.append('-i')
        if not isinstance(pciids, Path):
            pciids = Path(pciids)
        assert pciids.is_file(), 'ID database file not found'
        args.append(str(pciids.absolute()))

    if pcimap:
        args.append('-p')
        if not isinstance(pcimap, Path):
            pcimap = Path(pcimap)
        assert pcimap.is_file(), 'Kernel module mapping file not found'
        args.append(str(pcimap.absolute()))

    if file:
        args.append('-F')
        if not isinstance(file, Path):
            file = Path(file)
        assert file.is_file(), 'Hex dump file not found'
        args.append(str(file.absolute()))

    for key, value in pcilib_params.items():
        args.append('-O{}={}'.format(key, value))

    return subprocess.check_output(
        args,
        universal_newlines=True,
    )
