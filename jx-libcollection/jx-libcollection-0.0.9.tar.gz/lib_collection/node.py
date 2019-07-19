class Node(object):
    def __init__(self, v):
        self.v = v
        self.next = None

    def __str__(self):
        """
        >>> n = Node('a')
        >>> n
        Node('a')
        >>> n = Node(1)
        >>> n
        Node(1)
        """
        return 'Node({})'.format(repr(self.v))

    __repr__ = __str__
