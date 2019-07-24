from functools import reduce
from itertools import takewhile, dropwhile, chain
from typing import Any, Iterable, List, Reversible, Callable, Generator


def head(it: Iterable[Any]) -> Any:
    """
    Get top of iterable object

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.head([1, 2, 3])
        1
        >>> fpsm.head(range(1, 11))
        1
    """
    return next(iter(it))


def tail(it: Iterable[Any]) -> List[Any]:
    """
    Get anything but the beginning of an iterable object

    Args:
        it:

    Examples:
        >>> fpsm.tail([1, 2, 3])
        [2, 3]
        >>> fpsm.tail(range(1, 5))
        [2, 3, 4]
    """
    _, *i = it
    return i


def init(it: Iterable[Any]) -> List[Any]:
    """
    Get all but end of iterable object

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.init([1, 2, 3])
        [1, 2]
        >>> fpsm,init(range(5))
        [0, 1, 2, 3]
    """
    *i, _ = it
    return i


def last(it: Reversible[Any]) -> Any:
    """
    Get end of iterable object

    Args:
        it: Reversible(Iterable)) object

    Examples:
        >>> fpsm.last([1, 2, 3])
        3
        >>> fpsm.last('hello world')
        'd'
    """
    return next(iter(reversed(it)))


def take(n: int, it: Iterable[Any]) -> List[Any]:
    """
    Get a list of N elements from the beginning of the iterable object

    Args:
        n: Number of items to extract from the top
        it: Iterable object

    Examples:
        >>> fpsm.take(2, [1, 2, 3, 4, 5])
        [1, 2]
        >>> fpsm.take(3, map(lambda x: x ** 2, range(1, 10)))
        [1, 4, 9]
    """
    return list(it)[:n]


def null(it: Iterable[Any]) -> bool:
    """
    Return empty or boolean value of iterable object

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.null([])
        True
        >>> fpsm.null(range(100))
        False
    """
    return not list(it)


def foldl(func: Callable[[Any, Any], Any], it: Iterable[Any]):
    """
    Left-fold iterable object

    Args:
        func: Two arguments function
        it: Iterable object

    Examples:
        >>> fpsm.foldl(lambda x, y: x + y, range(11))
        55
    """
    return reduce(func, it, 0)


def foldr(func: Callable[[Any, Any], Any], it: Reversible[Any]):
    """
    Right-fold iterable object

    Args:
        func: Two arguments function
        it: Reversible(Iterable) object

    Examples:
        >>> fpsm.foldr(lambda x ,y: x - y, range(11))
        5
    """
    return reduce(lambda x, y: func(y, x), reversed(it), 0)


def concat(*it: Iterable[Any]) -> Any:
    """
    Concatenation of iterable objects

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.concat([1, 2, 3], [4, 5, 6])
        [1, 2, 3, 4, 5, 6]
    """
    return reduce(lambda x, y: x + y, map(list, it))


def concat_map(func: Callable[[Any], Any], *it: Iterable[Any]) -> Any:
    """
    Apply function recursively to iterable object and concat

    Args:
        func: One argument function
        it: Iterable object

    Examples:
        >>> fpsm.concat_map(lambda x: [0, x], [1, 2], [3, 4])
        [0, 1, 0, 2, 0, 3, 0, 4]
    """
    return concat(*list(map(func, concat(*it))))


def product(it: Iterable[Any]) -> Any:
    """
    Convolution product of iterable object

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.product(range(6))
        120
    """
    return reduce(lambda x, y: x * y, it)


def drop(n: int, it: Iterable[Any]) -> List[Any]:
    """
    Return a list of N elements drop from the iterable object

    Args:
        n: Number to drop from the top
        it: Iterable object

    Examples:
        >>> fpsm.drop(3, [1, 2, 3, 4, 5])
        [4, 5]
    """
    return list(it)[n:]


def split_at(n: int, it: Iterable[Any]) -> List[List[Any]]:
    """
    Split an iterable object into N elements

    Args:
        n: Split number
        it: Iterable object

    Examples:
        >>> fpsm.split_at(2, [1, 2, 3, 4, 5])
        [[1, 2], [3, 4, 5]]
    """
    return [take(n, it), drop(n, it)]


def span(func: Callable[[Any], bool], it: Iterable[Any]) -> List[List[Any]]:
    """
    Find the iterable object from the top and divide it into
    two by the element that does not satisfy the condition

    Args:
        func: One argument function that bool returns
        it: Iterable object

    Examples:
        >>> fpsm.span(lambda x: x < 3, [1, 2, 5, 1, 7])
        [[1, 2], [5, 1, 7]]

    """
    return [list(takewhile(func, it)), list(dropwhile(func, it))]


def elem(n: Any, it: Iterable[Any]) -> bool:
    """
    Determine if iterable object contains the given element

    Args:
        n: Value to validate
        it: Iterable object

    Examples:
        >>> fpsm.elem(2, range(10))
        True
        >>> fpsm.elem(1, range(2, 4))
        False
    """
    return n in list(it)


def not_elem(n: Any, it: Iterable[Any]) -> bool:
    """
    Determine if iterable object does not contain the given element

    Args:
        n: Value to validate
        it: Iterable object

    Examples:
        >>> fpsm.elem(2, range(10))
        False
        >>> fpsm.elem(1, range(2, 4))
        True
    """
    return n not in list(it)


def flatten(it: Iterable[Any]) -> List[Any]:
    """
    Convert multi-dimensional iterable object to one-dimensional list

    Args:
        it: Iterable object

    Examples:
        >>> fpsm.flatten([[1, 2], [3, 4, 5]])
        [1, 2, 3, 4, 5]
        >>> fpsm.flatten([[[1], [2, 4]]])
        [[1], [2, 4]]
    """
    return list(chain.from_iterable(it))


def infinite(n: int = 0) -> Generator:
    """
    Infinite generator

    Args:
        n: Initial value

    Examples:
        >>> inf = fpsm.infinite()
        >>> next(inf)
        0
        >>> inf = fpsm.infinite(1)
        >>> [next(inf) for _ in range(5)]
        [1, 2, 3, 4, 5]
    """
    while True:
        yield n
        n += 1
