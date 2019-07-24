class Node(object):

    def __init__(self, v):
        self.v = v
        self.next = None

    def __repr__(self):
        """
        >>> n = Node('a')
        >>> n
        Node('a')
        """
        return 'Node({})'.format(repr(self.v))


class SimpleLinkedQueue(object):

    def __init__(self):
        self.n = 0
        self.head = Node(None)

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q
        SimpleLinkedQueue(['a', 'b', 'c'])
        """
        return 'SimpleLinkedQueue([{}])'.format(', '.join(repr(i) for i in self))

    def __contains__(self, i):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> 'a' in q
        True
        >>> 'b' in q
        True
        >>> 'c' in q
        False
        """
        for item in self:
            if item == i:
                return True
        return False

    def __iter__(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> for i in q:
        ...     print(i)
        a
        b
        c
        """
        h = self.head
        while h.next is not None:
            h = h.next
            yield h.v

    def enqueue(self, i):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> len(q)
        1
        >>> q.enqueue('b')
        >>> len(q)
        2
        """
        n = Node(i)
        h = self.head
        while h.next is not None:
            h = h.next
        h.next = n
        self.n += 1

    def dequeue(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        """
        if len(self) == 0:
            raise IndexError('dequeue from empty queue')
        res = self.head.next.v
        self.head.next = self.head.next.next
        self.n -= 1
        return res 

    @property
    def top(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.top
        'a'
        """
        if len(self) == 0:
            raise IndexError('top from empty queue')
        return self.head.next.v


if __name__ == '__main__':
    import doctest
    doctest.testmod()
