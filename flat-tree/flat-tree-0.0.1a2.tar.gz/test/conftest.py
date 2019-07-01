import pytest

from flat_tree.accessor import FlatTreeAccessor


@pytest.fixture
def tree():
    return FlatTreeAccessor()


@pytest.fixture
def FlatTreeIterator():
    from flat_tree.iterator import FlatTreeIterator

    return FlatTreeIterator
