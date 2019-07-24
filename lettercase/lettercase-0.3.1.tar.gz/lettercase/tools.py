"""Utilities for making conversion easier."""

from contextlib import suppress
from functools import wraps
from typing import Any, Dict, FrozenSet, Generic, Iterable, Iterator, Mapping, MutableMapping, MutableSequence, \
    Optional, Set, Tuple, TypeVar, Union

from .converters import ConverterType, get_converter
from .letter_case import LetterCase, LetterCaseType, get_letter_case

__all__ = ["ConversionMemo",
           "MemoType",
           "memo_converter", "is_memo_converter",
           "convert_iter_items",
           "mut_convert_items", "mut_convert_keys"]

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class _InverseMappingWrapper(MutableMapping[K, V], Generic[K, V]):
    _forward: MutableMapping[K, V]
    _backward: MutableMapping[V, K]

    def __init__(self, forward: MutableMapping[K, V], backward: MutableMapping[V, K]) -> None:
        assert len(forward) == len(backward), "lengths need to match"

        self._forward = forward
        self._backward = backward

    def __setitem__(self, k: K, v: V) -> None:
        self._forward[k] = v
        self._backward[v] = k

    def __delitem__(self, k: K) -> None:
        v = self[k]
        del self._forward[k]
        del self._backward[v]

    def __getitem__(self, k: K) -> V:
        return self._forward[k]

    def __len__(self) -> int:
        return len(self._forward)

    def __iter__(self) -> Iterator[K]:
        return iter(self._forward)


TwoWayMemoTuple = Tuple[Dict[str, str], Dict[str, str]]


class ConversionMemo:
    """Specialised memoization class which keeps memo maps.

    The advantage of using this over a normal `dict` is that it automatically
    "learns" the reverse operation of a conversion (ex: "a_b" -> "aB" also
    learns "aB" -> "a_b").

    These results are stored completely separate though, to avoid accidentally
    converting the wrong way (if a text is already in the right case but because
    of the map it's flipped).
    """

    _memos: Dict[FrozenSet[LetterCase], TwoWayMemoTuple]

    def __init__(self) -> None:
        self._memos = {}

    def _get_memo_tuple(self, from_case: Optional[LetterCase], to_case: LetterCase) -> TwoWayMemoTuple:
        key = frozenset((from_case, to_case))
        try:
            memo_tuple = self._memos[key]
        except KeyError:
            memo_tuple = self._memos[key] = ({}, {})

        first_case, second_case = key
        if first_case is from_case:
            return memo_tuple
        else:
            return memo_tuple[1], memo_tuple[0]

    def get_memo(self, from_case: Optional[LetterCaseType], to_case: LetterCaseType) -> MutableMapping[str, str]:
        """Get the memo map which maps texts from `from_case` to the converted text in `to_case`

        Args:
            from_case: Case to convert from. Can be `None`.
            to_case: Case to convert to.

        Returns:
            A mutable mapping which is used to store `from_case` -> `to_case`
            conversions.
        """
        if from_case is not None:
            from_case = get_letter_case(from_case)
        to_case = get_letter_case(to_case)

        forward, backward = self._get_memo_tuple(from_case, to_case)
        return _InverseMappingWrapper(forward, backward)


MemoType = Union[ConversionMemo, Mapping[str, str], MutableMapping[str, str]]

MEMO_CONVERTER_FLAG = "__memoized__"


def memo_converter(converter: ConverterType, memo: Union[Mapping[str, str], MutableMapping[str, str]]) -> ConverterType:
    """Decorator which adds memoization to a converter.

    Args:
        converter: Converter to patch
        memo: Memoization mapping to use. If the mapping is mutable it will automatically be updated with new keys.

    Examples:
        >>> memo_data = {}
        >>> converter = memo_converter(get_converter("snake", "dromedary"), memo_data)
        >>> print(converter("snake_test"))
        snakeTest
        >>> print(memo_data)
        {'snake_test': 'snakeTest'}
    """

    @wraps(converter)
    def wrapper(text: str) -> str:
        try:
            return memo[text]
        except KeyError:
            pass

        new_text = converter(text)

        with suppress(Exception):
            memo[text] = new_text

        return new_text

    setattr(wrapper, MEMO_CONVERTER_FLAG, True)

    return wrapper


def is_memo_converter(converter: ConverterType) -> bool:
    """Check if a converter is memoized using `memo_converter`.

    Args:
        converter: Converter to check

    Returns:
        `True` if the converter is memoized, `False` otherwise.
    """
    return getattr(converter, MEMO_CONVERTER_FLAG, False)


def _get_converter(from_case: Optional[LetterCaseType], to_case: LetterCaseType,
                   memo: Optional[MemoType]) -> ConverterType:
    """Internal utility function to get a patched converter.

    Raises:
        ValueError: If no converter was found from `from_case` to `to_case`
    """
    converter = get_converter(from_case, to_case)
    if not converter:
        if from_case:
            text = f"No converter for {from_case} -> {to_case}"
        else:
            text = f"No general converter to {to_case}"

        raise ValueError(text)

    if memo is not None:
        if isinstance(memo, ConversionMemo):
            memo = memo.get_memo(from_case, to_case)

        converter = memo_converter(converter, memo)

    return converter


def convert_iter_items(iterable: Iterable[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                       memo: MemoType = None) -> Iterator[str]:
    """Patch an iterable so that all items are converted to the case.

    Args:
        iterable: Iterable to convert
        from_case: `LetterCase` to convert from, passing `None` will use a general converter.
        to_case: `LetterCase` to convert to
        memo: Memoization mapping to make conversion faster.
    """
    converter = _get_converter(from_case, to_case, memo)
    return map(converter, iterable)


def mut_convert_items(seq: MutableSequence[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                      memo: MemoType = None) -> None:
    """Convert all items in a mutable sequence to the given case."""
    converter = _get_converter(from_case, to_case, memo)

    for i, item in enumerate(seq):
        new_item = converter(item)
        if new_item != item:
            seq[i] = new_item


def mut_convert_keys(mapping: MutableMapping[str, Any], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                     memo: MemoType = None) -> None:
    """Convert all keys in a mutable mapping to the given case.

    Args:
        mapping: Mapping whose keys are to be converted
        from_case: Specify the case to convert from. If not provided a general converter is used.
        to_case: `LetterCase` to convert to
        memo: Memoization map to use.
    """
    converter = _get_converter(from_case, to_case, memo)

    original_keys: Set[str] = set(mapping.keys())

    for key in original_keys:
        new_key = converter(key)
        if new_key != key:
            mapping[new_key] = mapping.pop(key)
