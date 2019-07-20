class ResizingArrayQueue(object):

    def __init__(self, lst=None, capacity=2):
        self.capacity = capacity
        self.lst = [None] * self.capacity
        self.head = 0
        self.tail = 0
        self.n = 0

    def __len__(self):
        """
        >>> queue = ResizingArrayQueue()
        >>> len(queue)
        0
        >>> queue.enqueue('a')
        >>> len(queue)
        1
        >>> queue.enqueue('b')
        >>> len(queue)
        2
        """
        return self.n

    def __contains__(self, i):
        """
        >>> queue = ResizingArrayQueue()
        >>> 'a' in queue
        False
        >>> queue.enqueue('a')
        >>> queue.enqueue('b')
        >>> 'a' in queue
        True
        """
        for j in self:
            if j == i:
                return True
        return False

    def __iter__(self):
        """
        >>> queue = ResizingArrayQueue()
        >>> queue.enqueue('a')
        >>> queue.enqueue('b')
        >>> for i in queue:
        ...     print i
        ...
        a
        b
        """
        n = self.head
        for _ in range(len(self)):
            if n == self.capacity:
                n = 0
            yield self.lst[n]
            n += 1

    def __repr__(self):
        """
        >>> queue = ResizingArrayQueue()
        >>> queue.enqueue('a')
        >>> queue.enqueue('b')
        >>> queue
        ResizingArrayQueue(['a', 'b'])
        >>> print queue
        ResizingArrayQueue(['a', 'b'])
        """
        return 'ResizingArrayQueue([{}])'.format(', '.join(repr(i) for i in self))

    def enqueue(self, i):
        """
        >>> queue = ResizingArrayQueue()
        >>> queue.enqueue('a')
        >>> queue.enqueue('b')
        >>> queue.enqueue('c')
        >>> queue
        ResizingArrayQueue(['a', 'b', 'c'])
        >>> queue.capacity
        4
        """
        if len(self) == self.capacity:
            self._resize(self.capacity*2)

        if self.tail == self.capacity:
            self.tail = 0

        self.lst[self.tail] = i
        self.tail += 1
        self.n += 1

    def dequeue(self):
        """
        >>> queue = ResizingArrayQueue()
        >>> queue.dequeue()
        Traceback (most recent call last):
            ...
        IndexError: dequeue from empty queue
        >>> queue.enqueue('a')
        >>> queue.enqueue('b')
        >>> queue.enqueue('c')
        >>> queue.dequeue()
        'a'
        >>> queue.dequeue()
        'b'
        >>> queue.enqueue('d')
        >>> queue.enqueue('e')
        >>> queue.enqueue('f')
        >>> queue.lst
        ['e', 'f', 'c', 'd']
        >>> queue.enqueue('g')
        >>> queue.capacity
        8
        >>> queue.dequeue()
        'c'
        >>> queue.dequeue()
        'd'
        >>> queue.dequeue()
        'e'
        >>> queue.dequeue()
        'f'
        >>> queue.capacity
        4
        >>> queue.dequeue()
        'g'
        >>> queue.capacity
        2
        """
        if len(self) == 0:
            raise IndexError('dequeue from empty queue')

        if len(self) * 4 <= self.capacity:
            self._resize(self.capacity/2)

        if self.head == self.capacity:
            self.head = 0

        res = self.lst[self.head]
        self.head += 1
        self.n -= 1
        return res

    @property
    def top(self):
        """
        >>> queue = ResizingArrayQueue()
        >>> queue.top
        Traceback (most recent call last):
            ...
        IndexError: top from empty queue
        >>> queue.enqueue('a')
        >>> queue.top
        'a'
        >>> queue.enqueue('b')
        >>> queue.top
        'a'
        >>> queue.dequeue()
        'a'
        >>> queue.top
        'b'
        """
        if len(self) == 0:
            raise IndexError('top from empty queue')
        return self.lst[self.head]

    def _resize(self, n):
        q = ResizingArrayQueue(capacity=n)
        for e in self:
            q.enqueue(e)

        self.capacity = q.capacity
        self.lst = q.lst
        self.head = q.head
        self.tail = q.tail
        self.n = q.n
