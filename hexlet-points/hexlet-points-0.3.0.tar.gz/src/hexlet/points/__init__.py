# coding: utf-8

"""SICP'ish Points implemented in Python using hexlet.pairs."""

from typing import Optional

from hexlet import pairs

__all__ = (   # noqa: WPS317
    'make',
    'get_x', 'get_y', 'get_quadrant',
    'to_string',
)


def make(x: int, y: int) -> pairs.Pair:
    """Make a new point from pair of coordinates."""
    return pairs.cons(x, y)


def get_x(point: pairs.Pair) -> int:
    """Return an X coordinate of the point."""
    return pairs.car(point)


def get_y(point: pairs.Pair) -> int:
    """Return an Y coordinate of the point."""
    return pairs.cdr(point)


def to_string(point: pairs.Pair) -> str:
    """Return a string representation of the point."""
    return repr((get_x(point), get_y(point)))


def get_quadrant(point: pairs.Pair) -> Optional[int]:
    """Return a quadrant number for the point."""
    x, y = get_x(point), get_y(point)
    if not x or not y:
        return None
    return {
        (True, True): 1,
        (False, True): 2,
        (False, False): 3,
        (True, False): 4,
    }[(x > 0, y > 0)]
