class Node(object):

    def __init__(self, v):
        self.v = v
        self.next = None

    def __repr__(self):
        """
        >>> n = Node('a')
        >>> n
        Node('a')
        >>> print(n)
        Node('a')
        """
        return 'Node({})'.format(repr(self.v))


class LinkedQueue(object):

    def __init__(self):
        self.n = 0
        self.head = None
        self.tail = None

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q
        LinkedQueue(['a', 'b', 'c'])
        >>> print(q)
        LinkedQueue(['a', 'b', 'c'])
        """
        return 'LinkedQueue([{}])'.format(', '.join(repr(i) for i in self))

    def __iter__(self):
        """
        >>> q = LinkedQueue()
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
        while h:
            yield h.v
            h = h.next

    def __contains__(self, i):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('c')
        >>> 'a' in q
        True
        >>> 'b' in q
        False
        """
        for j in self:
            if i == j:
                return True
        return False


    def enqueue(self, item):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> len(q)
        2
        """
        n = Node(item)
        if self.head is None:
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            self.tail = n
        self.n += 1

    def dequeue(self):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.dequeue()
        'c'
        """
        if len(self) == 0:
            raise IndexError('dequeue from empty queue')
        res = self.head.v
        self.head = self.head.next
        self.n -= 1
        return res

    @property
    def top(self):
        """
        >>> q = LinkedQueue()
        >>> q.top
        Traceback (most recent call last):
            ...
        IndexError: top from empty queue

        """
        if len(self) == 0:
            raise IndexError('top from empty queue')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
