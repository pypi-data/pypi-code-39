# coding: utf-8
from demo_classic_usage import foo, bar, baz

if __name__ == '__main__':
    foo()  # emit: nothing
    bar()  # emit nothing
    baz()  # emit: FutureWarning
