from .point import ECCPoint


class Curve:
    @property
    def p(self)->int:
        raise NotImplementedError()

    @property
    def a(self)->int:
        raise NotImplementedError()

    @property
    def b(self)->int:
        raise NotImplementedError()

    @property
    def n(self)->int:
        raise NotImplementedError()

    @property
    def h(self)->int:
        raise NotImplementedError()

    @property
    def G(self)->ECCPoint:
        raise NotImplementedError()
