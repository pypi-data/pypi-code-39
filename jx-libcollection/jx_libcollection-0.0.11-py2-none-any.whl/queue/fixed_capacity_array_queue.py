class FixedCapacityArrayQueue(object):

    def __init__(self, lst=None, capacity=5):
        """
        >>> q = FixedCapacityArrayQueue(['a', 'b', 'c'])
        >>> q
        FixedCapacityArrayQueue(['a', 'b', 'c'])
        """
        self.capacity = capacity
        self.lst = [None] * capacity
        self.n = 0
        self.head = 0
        self.tail = 0

        if lst:
            q = FixedCapacityArrayQueue(capacity=capacity)
            for i in lst:
                q.enqueue(i)
            self.lst = q.lst
            self.n = q.n
            self.head = q.head
            self.tail = q.tail

    def __len__(self):
        """
        >>> q = FixedCapacityArrayQueue(capacity=4)
        >>> len(q)
        0
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> len(q)
        1
        >>> q.enqueue('d')
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> len(q)
        4
        """
        return self.n

    def __contains__(self, i):
        """
        >>> q = FixedCapacityArrayQueue(capacity=4)
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
        >>> q = FixedCapacityArrayQueue(capacity=4)
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.enqueue('d')
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> q.lst
        ['e', 'f', 'c', 'd']
        >>> for i in q:
        ...     print i
        ...
        c
        d
        e
        f
        """
        n = self.head
        for i in range(len(self)):
            yield self.lst[n]
            n = (n+1) % self.capacity

    def __repr__(self):
        """
        >>> q = FixedCapacityArrayQueue(capacity=4)
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.enqueue('c')
        >>> q.dequeue()
        'a'
        >>> q.dequeue()
        'b'
        >>> q.enqueue('d')
        >>> q.enqueue('e')
        >>> q.enqueue('f')
        >>> q.lst
        ['e', 'f', 'c', 'd']
        >>> q
        FixedCapacityArrayQueue(['c', 'd', 'e', 'f'])
        """
        return 'FixedCapacityArrayQueue([{}])'.format(', '.join(repr(i) for i in self))

    def enqueue(self, i):
        """
        >>> q = FixedCapacityArrayQueue(capacity=0)
        >>> q.enqueue('a')
        Traceback (most recent call last):
            ...
        IndexError: queue overflow
        >>> q = FixedCapacityArrayQueue(capacity=2)
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.lst
        ['a', 'b']
        >>> q.tail
        0
        """
        if len(self) == self.capacity:
            raise IndexError('queue overflow')

        self.lst[self.tail]= i
        self.tail = (self.tail + 1) % self.capacity
        self.n += 1

    def dequeue(self):
        """
        >>> q = FixedCapacityArrayQueue(capacity=0)
        >>> q.dequeue()
        Traceback (most recent call last):
            ...
        IndexError: queue underflow
        >>> q = FixedCapacityArrayQueue(capacity=2)
        >>> q.enqueue('a')
        >>> q.enqueue('b')
        >>> q.dequeue()
        'a'
        >>> q.enqueue('c')
        >>> q.dequeue()
        'b'
        >>> q.enqueue('d')
        >>> q.dequeue()
        'c'
        """
        if len(self) == 0:
            raise IndexError('queue underflow')
        res = self.lst[self.head]
        self.head = (self.head + 1) % self.capacity
        self.n -= 1
        return res

    @property
    def top(self):
        """
        >>> q = FixedCapacityArrayQueue(capacity=3)
        >>> q.top
        Traceback (most recent call last):
            ...
        IndexError: queue underflow
        >>> q.enqueue('a')
        >>> q.top
        'a'
        >>> q.enqueue('b')
        >>> q.top
        'a'
        """
        if len(self) == 0:
            raise IndexError('queue underflow')
        return self.lst[self.head]
