# -*- coding: utf-8 -*-


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


if __name__ == "__main__":
    print(is_number(4))
    print(is_number(4.5))
    print(is_number(1e-4))
    print(is_number('st'))
    print(is_number(' '))
