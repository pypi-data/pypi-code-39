class MyFbase(object):
    def __init__(self, base: str):
        super(MyFbase, self).__init__()
        self.base = [c for c in base]
        self._numeric_base = len(self.base)
        if len(set(self.base)) != len(self.base):
            raise ValueError("Your base has duplicate elements.")

    def encode(self, decimal_number: int) -> str:
        """
        >>> m.encode(0)
        'a'
        >>> m.encode(1)
        'b'
        >>> m.encode(2)
        'c'
        >>> m.encode(3)
        'ba'
        """

        if decimal_number < 0:
            raise ValueError("Can convert only positive integers")
        if decimal_number == 0:
            return self.base[0]

        digits = []
        while decimal_number > 0:
            digits.append(decimal_number % self._numeric_base)
            decimal_number //= self._numeric_base

        return "".join([self.base[e] for e in digits[::-1]])

    def decode(self, code: str) -> int:
        """
        >>> m.decode('a')
        0
        >>> m.decode('b')
        1
        >>> m.decode('c')
        2
        >>> m.decode('ba')
        3
        """

        out = 0
        reversed_code = code[::-1]
        for index, char in enumerate(reversed_code, start=0):
            out += self.base.index(char) * (self._numeric_base ** index)
        return out


if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs={"m": MyFbase("abc")})
