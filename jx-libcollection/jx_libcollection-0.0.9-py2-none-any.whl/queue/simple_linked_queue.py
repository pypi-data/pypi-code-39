from lib_collection.node import Node


class SimpleLinkedQueue(object):

    def __init__(self, lst=None):
        """
        >>> q = SimpleLinkedQueue(['a', 2, 'c'])
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
        SimpleLinkedQueue(['c', 4, 'e'])
        """
        self.n = 0
        self.head = Node(None)

        if lst:
            queue = SimpleLinkedQueue()
            for e in lst:
                queue.enqueue(e)
            self.n = queue.n
            self.head = queue.head

    def __len__(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> len(q)
        0
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> len(q)
        3
        >>> q.dequeue()
        'a'
        >>> len(q)
        2
        """
        return self.n

    def __contains__(self, i):
        """
        >>> q = SimpleLinkedQueue()
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
        >>> q = SimpleLinkedQueue()
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
        while n.next is not None:
            n = n.next
            yield n.v

    def __repr__(self):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue(2)
        >>> q.enqueue('c')
        >>> q
        SimpleLinkedQueue(['a', 2, 'c'])
        >>> print q
        SimpleLinkedQueue(['a', 2, 'c'])
        """
        return 'SimpleLinkedQueue([{}])'.format(', '.join(repr(i) for i in self))

    def enqueue(self, i):
        """
        >>> q = SimpleLinkedQueue()
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        """
        node = Node(i)
        n = self.head
        while n.next is not None:
            n = n.next
        n.next = node
        self.n += 1

    def dequeue(self):
        """
        >>> q = SimpleLinkedQueue()
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
        IndexError: dequeue from empty queue
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
        >>> q.top
        Traceback (most recent call last):
            ...
        IndexError: top from empty queue
        >>> q.enqueue('a')
        >>> q.top
        'a'
        >>> q.enqueue('b')
        >>> q.top
        'a'
        """
        if len(self) == 0:
            raise IndexError('top from empty queue')
        return self.head.next.v
