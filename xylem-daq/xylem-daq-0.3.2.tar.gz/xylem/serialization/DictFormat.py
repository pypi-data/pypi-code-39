'''
A basic data formatter which converts to and from a string
representation of a dict. Sort of like JSON.

'''

import ast

def toBytes(data):
    '''
    Formats data into bytes.

    Converts the data to a dict, calls a string representation, then
    encodes the string in utf-8 bytes.

    '''
    return str(dict(data)).encode('utf-8')

def fromBytes(data):
    '''
    Formats the bytes into a python Dict.

    Evaluates the bytes (decoded into a string) into a python Dict using
    a safe evaluation method from the ast module.

    '''
    return ast.literal_eval(data.decode('utf-8'))
