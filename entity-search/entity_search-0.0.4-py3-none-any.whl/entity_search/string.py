import nltk
import krovetz

def porter_stemmer(tokens):
    """ Stem words using porter algorithm
    Args:
        tokens: list of tokens
    Response:
        A list of stemmed tokens
    """
    ps = nltk.stem.PorterStemmer()
    return [ps.stem(token) for token in tokens ]

# We create one instance of this class as it is very slow to load it
ks = krovetz.PyKrovetzStemmer()

def krovetz_stemmer(tokens):
    """ Stem words using Krovetz algorithm
    Args:
        tokens: list of tokens
    Response:
        A list of stemmed tokens
    """
    return [ks.stem(token) for token in tokens ]

def no_stemmer(tokens):
    """ Dummy funcion for stemming
    Args:
        tokens: list of tokens
    Response:
        Same as the input list
    """
    return tokens

def join_str(c):
    """ Fast function for concatenating strings.
    By default, it uses a single white space as seperator.
    Args:
        c: list of strings
    Response:
        A concatenation of the strings in c
    """
    return " ".join(c)
