
def random_module_name():
    import random
    import string
    alpha = string.digits + string.ascii_lowercase
    n = random.randrange(2**126, 2**128)
    n, r = divmod(n, 26)
    res = alpha[10 + r]
    while n:
        n, r = divmod(n, 36)
        res += alpha[r]
    return res

if __name__ == '__main__':
    print(random_module_name())