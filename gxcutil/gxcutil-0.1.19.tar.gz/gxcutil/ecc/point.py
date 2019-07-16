from ..utils import mod_inv


class ECCPoint:
    def __init__(self, x: int, y: int = None, *args):
        if len(args) == 1:
            curve = args[0]

            self._p = curve.p
            self._a = curve.a
            self._b = curve.b
        else:
            self._p = args[0]
            self._a = args[1]
            self._b = args[2]

        self._x = x % self._p
        if y is None:
            y_2 = (pow(self._x, 3, self._p) + self._a * self._x + self._b) % self._p
            self._y = pow(y_2, (self._p + 1) >> 2, self._p)
        else:
            self._y = y % self._p

    @property
    def x(self)->int:
        return self._x

    @property
    def y(self)->int:
        return self._y

    def __neg__(self)->'ECCPoint':
        return ECCPoint(self._x, -self._y, self._p, self._a, self._b)

    def __add__(self, o: 'ECCPoint')->'ECCPoint' or None:
        if o is None:
            return None

        if (o._x - self._x) % self._p == 0:
            return None

        t = ((o._y - self._y) * mod_inv(o._x - self._x, self._p)) % self._p
        x = t * t - self._x - o._x
        y = t * (self._x - x) - self._y

        return ECCPoint(x, y, self._p, self._a, self._b)

    def __sub__(self, o: 'ECCPoint')->'ECCPoint' or None:
        if o is None:
            return None

        if (o._x - self._x) % self._p == 0:
            return None

        t = ((o._y + self._y) * mod_inv(self._x - o._x, self._p)) % self._p
        x = t * t - self._x - o._x
        y = t * (self._x - x) - self._y

        return ECCPoint(x, y, self._p, self._a, self._b)

    def __eq__(self, o: 'ECCPoint')->bool:
        return self._x == o._x and self._y == o._y

    def double(self)->'ECCPoint' or None:
        if self._y == 0:
            return None

        t = (((3 * self._x * self._x + self._a) % self._p) * mod_inv(2 * self._y, self._p)) % self._p
        x = t * t - 2 * self._x
        y = t * (self._x - x) - self._y

        return ECCPoint(x, y, self._p, self._a, self._b)

    def multiply(self, n: int, cache: list or None = None)->'ECCPoint' or None:
        if cache is None:
            w_size = 1
            cache = [None, self]
        else:
            w_size = len(cache).bit_length() - 1
        w = (1 << w_size) - 1

        r = None
        d = []
        n_size = (n.bit_length() + w_size - 1) // w_size
        for _ in range(n_size):
            d.append(n & w)
            n >>= w_size

        for di in reversed(d):
            if r is not None:
                for _ in range(w_size):
                    r = r.double()

            if di == 0:
                continue

            if r is None:
                r = cache[di]
            else:
                r = r + cache[di]
                if r is None:
                    return r

        return r
