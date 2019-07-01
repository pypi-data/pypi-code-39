"""An accessor for navigating flat trees."""

__all__ = ['FlatTreeAccessor']

from typing import List, Optional


class FlatTreeAccessor:
    """A flat tree accessor."""

    def index(self, depth: int, offset: int) -> int:
        """The tree index specified by the depth and offset.

        :param depth: The depth of the tree
        :param offset: The offset from left hand side of the tree
        """
        return ((1 + (2 * offset)) * (2 ** depth)) - 1

    def offset(self, index: int, depth: Optional[int] = None) -> int:
        """The offset of given index from the left hand side of the tree.

        :param index: The tree index
        :param depth: The depth of the tree
        """
        if not (index & 1):
            return int(index / 2)

        if depth is None:
            depth = self.depth(index)

        return int((((index + 1) / (2 ** depth)) - 1) / 2)

    def depth(self, index: int) -> int:
        """The depth of the given index in the tree.

        :param index: The tree index
        """
        depth = 0

        index += 1
        while not (index & 1):
            depth += 1
            index = index >> 1

        return depth

    def parent(self, index: int, depth: Optional[int] = None) -> int:
        """The index of the parent relative to the given index.

        :param index: The index relative to the parent
        :param depth: The depth of the index
        """
        if depth is None:
            depth = self.depth(index)

        offset = self.offset(index, depth)

        return self.index(depth + 1, int((offset - (offset & 1)) / 2))

    def sibling(self, index: int, depth: Optional[int] = None) -> int:
        """The index of the sibling relative to the given index.

        :param index: The index relative to the sibling
        :param depth: The depth of the index
        """
        if depth is None:
            depth = self.depth(index)

        offset = self.offset(index, depth)
        offset = offset - 1 if (offset & 1) else offset + 1

        return self.index(depth, offset)

    def children(self, index: int, depth: Optional[int] = None) -> List[int]:
        """All children relative to the given index.

        :param index: The parent index
        :param depth: The depth of the index
        """
        if not (index & 1):
            return []

        if not depth:
            depth = self.depth(index)

        offset = self.offset(index, depth) * 2

        return [
            self.index((depth - 1), offset),
            self.index((depth - 1), (offset + 1)),
        ]

    def spans(self, index: int, depth: Optional[int] = None) -> List[int]:
        """The span of the tree.

        :param index: The index of the root
        :param depth: The depth of the index
        """
        if not (index & 1):
            return [index, index]

        if not depth:
            depth = self.depth(index)

        offset = self.offset(index, depth)
        width = 2 ** (depth + 1)

        return [(offset * width), ((offset + 1) * width) - 2]

    def left_span(self, index: int, depth: Optional[int] = None) -> int:
        """The leftmost span of the tree.

        :param index: The index of the tree root
        :param depth: The depth of the index
        """
        if not (index & 1):
            return index

        if not depth:
            depth = self.depth(index)

        return self.offset(index, depth) * (2 ** (depth + 1))

    def right_span(self, index: int, depth: Optional[int] = None) -> int:
        """The rightmost span of the tree.

        :param index: The index of the tree root
        :param depth: The depth of the index
        """
        if not (index & 1):
            return index

        if not depth:
            depth = self.depth(index)

        return (self.offset(index, depth) + 1) * (2 ** (depth + 1)) - 2

    def count(self, index: int, depth: Optional[int] = None) -> int:
        """The number of nodes a tree contains.

        :param index: The index of the root of the tree
        :param depth: The depth of the root of the tree
        """
        if not (index & 1):
            return 1

        if not depth:
            depth = self.depth(index)

        return (2 ** (depth + 1)) - 1

    def full_roots(self, index: int) -> List[int]:
        """All full roots within the tree.

        :param index: The index of the root of the tree
        """
        if index & 1:
            message = 'Roots only available for tree depth 0'
            raise ValueError(message)

        roots: List[int] = []

        index = int(index / 2)
        offset, factor = 0, 1

        while True:
            if not index:
                return roots

            while (factor * 2) <= index:
                factor = factor * 2

            roots.append((offset + factor) - 1)

            offset = (offset + 2) * factor
            index = index - factor
            factor = 1

    def left_child(self, index: int, depth: Optional[int] = None) -> int:
        """The left child of the given index.

        :param index: The index of the tree
        :param depth: The depth of the tree
        """
        if not (index & 1):
            return -1

        if not depth:
            depth = self.depth(index)

        return self.index((depth - 1), (self.offset(index, depth) * 2))

    def right_child(self, index: int, depth: Optional[int] = None) -> int:
        """The right child of the given index.

        :param index: The index of the tree
        :param depth: The depth of the tree
        """
        if not (index & 1):
            return -1

        if not depth:
            depth = self.depth(index)

        return self.index((depth - 1), (1 + (self.offset(index, depth) * 2)))
