"""Stateful iterator for flat trees."""

__all__ = ['FlatTreeIterator']

import attr

from flat_tree.accessor import FlatTreeAccessor


@attr.s(auto_attribs=True)
class FlatTreeIterator:
    """Stateful iterator for flat trees."""

    index: int = 0
    offset: int = 0
    factor: int = 0
    accessor: FlatTreeAccessor = FlatTreeAccessor()

    def __attrs_post_init__(self):
        self.seek(self.index)

    def next(self) -> int:
        """The next index in the tree."""
        self.offset += 1
        self.index += self.factor
        return self.index

    def prev(self) -> int:
        """The previous index in the tree."""
        if not self.offset:
            return self.index

        self.offset -= 1
        self.index = self.factor

        return self.index

    def seek(self, index: int) -> None:
        """Move iterator to the given index.

        :param index: The index to move to
        """
        self.index = index

        if self.index & 1:
            self.offset = self.accessor.offset(index)
            self.factor = 2 ** (self.accessor.depth(index) + 1)
        else:
            self.offset = int(index / 2)
            self.factor = 2

    def parent(self) -> int:
        """Move iterator to the parent index."""
        if self.offset & 1:
            self.index -= int(self.factor / 2)
            self.offset = int((self.offset - 1) / 2)
        else:
            self.index += int(self.factor / 2)
            self.offset = int(self.offset / 2)

        self.factor *= 2

        return self.index

    def left_child(self) -> int:
        """Move iterator to the left child."""
        if self.factor == 2:
            return self.index

        self.factor = int(self.factor / 2)
        self.index -= int(self.factor / 2)
        self.offset *= 2

        return self.index

    def right_child(self) -> int:
        """Move iterator to the right child."""
        if self.factor == 2:
            return self.index

        self.factor = int(self.factor / 2)
        self.index += int(self.factor / 2)
        self.offset = (2 * self.offset) + 1

        return self.index

    def left_span(self) -> int:
        """Move iterator to the left span."""
        self.index = int(self.index - (self.factor / 2)) + 1
        self.offset = int(self.index / 2)
        self.factor = 2
        return self.index

    def right_span(self) -> int:
        """Move iterator to the right span."""
        self.index = int((self.index - self.factor) / 2) - 1
        self.offset = int(self.index / 2)
        self.factor = 2
        return self.index

    def sibling(self) -> int:
        """Move iterator to the sibling."""
        return self.next() if self.is_left() else self.prev()

    def is_left(self) -> bool:
        """Is this index a left sibling?"""
        return not self.offset & 1

    def is_right(self) -> bool:
        """Is this index a right sibling?"""
        return not self.is_left()
