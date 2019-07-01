def test_iter_from_leaf(FlatTreeIterator):
    tree_iter = FlatTreeIterator()

    assert tree_iter.index == 0
    assert tree_iter.parent() == 1
    assert tree_iter.parent() == 3
    assert tree_iter.parent() == 7
    assert tree_iter.right_child() == 11
    assert tree_iter.left_child() == 9
    assert tree_iter.next() == 13
    assert tree_iter.left_span() == 12


def test_iter_not_from_leaf(FlatTreeIterator):
    tree_iter = FlatTreeIterator(index=1)

    assert tree_iter.index == 1
    assert tree_iter.parent() == 3
    assert tree_iter.parent() == 7
    assert tree_iter.right_child() == 11
    assert tree_iter.left_child() == 9
    assert tree_iter.next() == 13
    assert tree_iter.left_span() == 12
