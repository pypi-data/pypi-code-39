# coding: utf-8

"""SICP'ish Points implemented in Python using hexlet.pairs."""

from hexlet import pairs

__all__ = (   # noqa: WPS317
    'make',
    'get_x', 'get_y',
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
