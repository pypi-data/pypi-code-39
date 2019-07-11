"""Common standalone utility functions."""

from iotile.core.exceptions import ArgumentError

def convert_axis(in_axis):
    """Convert a numeric axis identifier to/from a string.

    Args:
        in_axis (str or int): The numerical or string axis

    Returns:
        int or str: The correspond integer or string axis name.
    """

    axes = {
        0: 'x',
        1: 'y',
        2: 'z'
    }

    reverse_axes = {
        'x': 0,
        'y': 1,
        'z': 2
    }

    if isinstance(in_axis, int):
        result = axes.get(in_axis, None)
    else:
        result = reverse_axes.get(in_axis, None)

    if result is None:
        raise ArgumentError("Invalid axis code", axis=in_axis)

    return result
