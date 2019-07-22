class Node(object):

    def __init__(self, v):
        self.v = v
        self.next = None

    def __repr__(self):
        """
        >>> n = Node('a')
        >>> n
        Node('a')
        >>> n = Node(1)
        >>> n
        Node(1)
        >>> print(n)
        Node(1)
        """
        return 'Node({})'.format(repr(self.v))
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
