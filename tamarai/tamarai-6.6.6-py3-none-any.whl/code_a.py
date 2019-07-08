
import random
import time
import math

# colors:
COLOR_END = "\033[0m"
COLOR_GREEN = "\033[94m"


def fib(x):
    """
    :returns an array of first x fib numbers
    :param x: length of to-be-found array
    :return: array of first x fib numbers
    """
    if type(x) != int:
        raise Exception("Input variable must be a positive int")
    if x < 0:
        raise Exception("Input variable must be a positive int")
    result = []
    a = 0
    b = 1
    c = 1
    while len(result) != x:
        result.append(a)
        a = b
        b = c
        c = a + b
    return result


def yesno():
    choices = (
        "Maybe",
        "Yes",
        "No",
        "Probably",
        "Probably not",
        "Perhaps",
        "Nah",
        )
    return random.choice(choices)


def line_print(sentence):
    result = ""
    sentence = sentence.upper()
    for i in sentence:
        result += i + "\n"
    return result


def self_destruct(close=False):
    print("Initiating self destruct sequence . . .")
    animation = "|/-\\"
    for i in range(30 + random.randint(0, 15)):
        print(end="\r")
        print(animation[i % len(animation)], end="")
        time.sleep(0.1)
    print("\rDone, closing all baklava processes", end="")
    if close:
        quit()


def laser(sec=20):
    spaces = ""
    for i in range(sec):
        spaces += " "
        print(end="\r")
        print(COLOR_GREEN + spaces + "-" + COLOR_END, end="")
        time.sleep(0.1)
    print("\r", end="\r")


def lang(string, added="b", letters=("a", "e", "i", "o", "u")):
    out = ""
    for letter in string:
        if letter in letters:
            out += letter + added + letter
        else:
            out += letter
    return out


def avg(*args):
    sm = 0
    for i in args:
        sm += i
    return sm/len(args)


def vector2abs(a, b):
    c = a**2 + b**2
    return math.sqrt(c)


def vector3abs(a, b, c):
    d = a**2 + b**2 + c**2
    return math.sqrt(d)


if __name__ == '__main__':
    print()
