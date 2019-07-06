# coding: utf-8

import warnings


def foo():
    warnings.warn("Deprecation of foo", DeprecationWarning)


def bar():
    warnings.warn("Pending deprecation of foo", PendingDeprecationWarning)


def baz():
    warnings.warn("Future deprecation of foo", FutureWarning)


if __name__ == '__main__':
    foo()  # emit: DeprecationWarning
    bar()  # emit nothing
    baz()  # emit: FutureWarning
