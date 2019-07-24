# coding: utf-8

"""SICP'ish functional pairs implemented in Python."""

from typing import Any, Callable, TypeVar, Union

__all__ = ('Pair', 'cons', 'car', 'cdr', 'is_pair', 'to_string')


A = TypeVar('A')
B = TypeVar('B')

Pair = Callable[[bool], Union[A, B]]


def cons(a: A, b: B) -> Pair:
    """Create a new pair."""
    def pair(car_is_need):
        if car_is_need:
            return a
        return b
    return pair


def car(pair: Pair) -> A:
    """Return a first element of pair."""
    return pair(True)


def cdr(pair: Pair) -> B:
    """Return a second element of pair."""
    return pair(False)


def is_pair(arg: Any) -> bool:
    """Check that arg is a pair."""
    return callable(arg)


def to_string(pair: Pair) -> str:
    """Convert a pair to the str."""
    return repr((car(pair), cdr(pair)))
