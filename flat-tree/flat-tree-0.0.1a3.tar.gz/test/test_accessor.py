import pytest


def test_index(tree):
    assert tree.index(0, 0) == 0
    assert tree.index(0, 1) == 2
    assert tree.index(0, 2) == 4


def test_depth(tree):
    assert tree.depth(5) == 1
    assert tree.depth(3) == 2
    assert tree.depth(4) == 0


def test_offset(tree):
    assert tree.offset(0) == 0
    assert tree.offset(1) == 0
    assert tree.offset(2) == 1
    assert tree.offset(3) == 0
    assert tree.offset(4) == 2

    assert isinstance(tree.offset(0), int)


def test_parent(tree):
    assert tree.index(1, 0) == 1
    assert tree.index(1, 1) == 5
    assert tree.index(2, 0) == 3

    assert tree.parent(0) == 1
    assert tree.parent(2) == 1
    assert tree.parent(1) == 3


def test_sibling(tree):
    assert tree.sibling(0) == 2
    assert tree.sibling(2) == 0
    assert tree.sibling(1) == 5
    assert tree.sibling(5) == 1


def test_children(tree):
    assert tree.children(0) == []
    assert tree.children(1) == [0, 2]
    assert tree.children(3) == [1, 5]
    assert tree.children(9) == [8, 10]


def test_count(tree):
    assert tree.count(0) == 1
    assert tree.count(1) == 3
    assert tree.count(3) == 7
    assert tree.count(5) == 3
    assert tree.count(23) == 15
    assert tree.count(27) == 7


def test_spans(tree):
    assert tree.spans(0) == [0, 0]
    assert tree.spans(1) == [0, 2]
    assert tree.spans(3) == [0, 6]
    assert tree.spans(23) == [16, 30]
    assert tree.spans(27) == [24, 30]


def test_left_span(tree):
    assert tree.left_span(0) == 0
    assert tree.left_span(1) == 0
    assert tree.left_span(3) == 0
    assert tree.left_span(23) == 16
    assert tree.left_span(27) == 24


def test_right_span(tree):
    assert tree.right_span(0) == 0
    assert tree.right_span(1) == 2
    assert tree.right_span(3) == 6
    assert tree.right_span(23) == 30
    assert tree.right_span(27) == 30


def test_full_roots(tree):
    assert tree.full_roots(0) == []
    assert tree.full_roots(2) == [0]
    assert tree.full_roots(8) == [3]
    assert tree.full_roots(20) == [7, 17]
    assert tree.full_roots(18) == [7, 16]
    assert tree.full_roots(16) == [7]

    with pytest.raises(ValueError):
        tree.full_roots(1)


def test_left_child(tree):
    assert tree.left_child(0) == -1
    assert tree.left_child(1) == 0
    assert tree.left_child(3) == 1


def test_right_child(tree):
    assert tree.right_child(0) == -1
    assert tree.right_child(1) == 2
    assert tree.right_child(3) == 5


def test_parent_big_index(tree):
    assert tree.parent(10000000000) == 10000000001


def test_child_parent_child(tree):
    child = 0

    for _ in range(50):
        child = tree.parent(child)
    assert child == 1125899906842623

    for _ in range(50):
        child = tree.left_child(child)
    assert child == 0
