from functools import reduce
from itertools import takewhile, dropwhile, chain
from typing import Any, Iterable, List, Reversible, Callable


def head(it: Iterable[Any]) -> Any:
    """Get top of iterable object"""
    return next(iter(it))


def tail(it: Iterable[Any]) -> List[Any]:
    """Get anything but the beginning of an iterable object"""
    _, *i = it
    return i


def init(it: Iterable[Any]) -> List[Any]:
    """Get all but end of iterable object"""
    *i, _ = it
    return i


def last(it: Reversible[Any]) -> Any:
    """Get end of iterable object"""
    return next(iter(reversed(it)))


def take(n: int, it: Iterable[Any]) -> List[Any]:
    """Get a list of N elements from the beginning of the iterable object"""
    return list(it)[:n]


def null(it: Iterable[Any]) -> bool:
    """Return empty or boolean value of iterable object"""
    return not list(it)


def foldl(func: Callable[[Any, Any], Any], it: Iterable[Any]):
    """Left-fold iterable object"""
    return reduce(func, it, 0)


def foldr(func: Callable[[Any, Any], Any], it: Reversible[Any]):
    """Right-fold iterable object"""
    return reduce(lambda x, y: func(y, x), reversed(it), 0)


def concat(*it: Iterable[Any]) -> Any:
    """Concatenation of iterable objects"""
    return reduce(lambda x, y: x + y, map(list, it))


def concat_map(func: Callable[[Any], Any], *it: Iterable[Any]) -> Any:
    """Apply function recursively to iterable object and concat"""
    return concat(*list(map(func, concat(*it))))


def product(it: Iterable[Any]) -> Any:
    """Convolution product of iterable object"""
    return reduce(lambda x, y: x * y, it)


def drop(n: int, it: Iterable[Any]) -> List[Any]:
    """Return a list of N elements drop from the iterable object"""
    return list(it)[n:]


def split_at(n: int, it: Iterable[Any]) -> List[List[Any], List[Any]]:
    """Split an iterable object into N elements"""
    return [take(n, it), drop(n, it)]


def span(func: Callable[[Any], bool], it: Iterable[Any]) -> List[List[Any], List[Any]]:
    """
    Find the iterable object from the top and divide it into
    two by the element that does not satisfy the condition
    """
    return [list(takewhile(func, it)), list(dropwhile(func, it))]


def elem(n: Any, it: Iterable[Any]) -> bool:
    """Determine if iterable object contains the given element"""
    return n in list(it)


def not_elem(n: Any, it: Iterable[Any]) -> bool:
    """Determine if iterable object does not contain the given element"""
    return n not in list(it)


def flatten(it: Iterable[Any]) -> List[Any]:
    """Convert multi-dimensional iterable object to one-dimensional list"""
    return list(chain.from_iterable(it))
