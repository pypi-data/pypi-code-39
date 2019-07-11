import re


def split_sentences(sentence):
    return re.split(r'[.!?]+ ', sentence), re.findall(r'[.!?]+ ', sentence)

def join_sentences(source, sentences, terminations):
    # startswith termination
    termination = re.match(r'^[.!?]+ .*', source)


# a = 'a.a a.1 1.a 1.1 a. 1. .a .1 . '
a = 'acessibilidade. usá-las'
print(re.sub(r'(?<=[a-zA-Z])(?=\.)', ' ', a))
