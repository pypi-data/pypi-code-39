from lib_collection.node import Node


class LinkedQueue(object):

    def __init__(self, lst=None):
        """
        >>> q = LinkedQueue(['a', 2, 'c'])
        >>> q.top
        'a'
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        2
        >>> len(q)
        1
        >>> q.enqueue(4)
        >>> q.enqueue('e')
        >>> q
        LinkedQueue(['c', 4, 'e'])
        """
        self.n = 0
        self.head = None
        self.tail = None

        if lst is not None:
            q = LinkedQueue()
            for e in lst:
                q.enqueue(e)
            self.n = q.n
            self.head = q.head
            self.tail = q.tail

    def __len__(self):
        """
        >>> q = LinkedQueue()
        >>> len(q)
        0
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> len(q)
        2
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> len(q)
        0
        """
        return self.n

    def __contains__(self, i):
        """
        >>> q = LinkedQueue()
        >>> 'a' in q
        False
        >>> q.enqueue('a')
        >>> 'a' in q
        True
        """
        for j in self:
            if i == j:
                return True
        return False

    def __iter__(self):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> for i in q:
        ...     print i
        ...
        a
        b
        c
        """
        n = self.head
        while n:
            yield n.v
            n = n.next

    def __repr__(self):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue(2)
        >>> q.enqueue('c')
        >>> q
        LinkedQueue(['a', 2, 'c'])
        >>> print q
        LinkedQueue(['a', 2, 'c'])
        """
        return 'LinkedQueue([{}])'.format(', '.join(repr(i) for i in self))

    def enqueue(self, i):
        """
        >>> q = LinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        """
        n = Node(i)
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
        >>> q.dequeue()
        Traceback (most recent call last):
            ...
        IndexError: queue underflowed
        """
        if self.head is None:
            raise IndexError('queue underflowed')
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
        IndexError: queue underflowed
        >>> q.enqueue('a')
        >>> q.top
        'a'
        >>> q.enqueue('b')
        >>> q.top
        'a'
        """
        if self.head is None:
            raise IndexError('queue underflowed')
        return self.head.v
