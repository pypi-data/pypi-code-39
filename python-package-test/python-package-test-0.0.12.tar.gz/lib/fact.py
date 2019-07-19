class InvalidFactorialError(RuntimeError):
    """Error generated if an invalid factorial input is given."""


def factorial(n: int) -> int:
    """Computes the factorial through a recursive algorithm."""
    if n < 0:
        raise InvalidFactorialError('n is less than zero: {}'.format(n))
    elif n == 0:
        return 1

    return n * factorial(n - 1)