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
        """
        return 'Node({})'.format(repr(self.v))


class LinkedStack(object):
    
    def __init__(self):
        self.n = 0
        self.head = Node(None)

    def __len__(self):
        return self.n

    def __repr__(self):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack.push('c')
        >>> stack
        LinkedStack(['c', 'b', 'a'])
        """
        return 'LinkedStack([{}])'.format(', '.join(repr(i) for i in self))

    def __contains__(self, item):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> 'a' in stack
        True
        >>> 'b' in stack
        True
        >>> 'c' in stack
        False
        """
        for i in self:
            if i == item:
                return True
        return False

    def __iter__(self):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> stack.push('c')
        >>> for i in stack:
        ...     print(i)
        c
        b
        a
        """
        n = self.head.next
        while n:
            yield n.v
            n = n.next

    def push(self, i):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> len(stack)
        1
        >>> stack.push('b')
        >>> len(stack)
        2
        """
        n = Node(i)
        n.next = self.head.next
        self.head.next = n 
        self.n += 1

    def pop(self):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> stack.push('b')
        >>> len(stack)
        2
        >>> stack.pop()
        'b'
        >>> len(stack)
        1
        >>> stack.pop()
        'a'
        >>> len(stack)
        0
        """
        if len(self) == 0:
            raise IndexError('pop from empty stack')
        n = self.head.next
        self.head.next = n.next
        self.n -= 1
        return n.v
    
    @property
    def top(self):
        """
        >>> stack = LinkedStack()
        >>> stack.push('a')
        >>> stack.top
        'a'
        """
        if len(self) == 0:
            raise IndexError('pop from empty stack')
        return self.head.next.v


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    
