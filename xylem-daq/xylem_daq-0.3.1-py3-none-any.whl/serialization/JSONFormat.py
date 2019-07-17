'''
A data formatter for converting to and from a JSON representation.

'''
import json

def toBytes(data):
    '''
    Formats data into bytes (str in Python 2) in JSON format.

    '''
    return json.dumps(data).encode('utf-8')

def fromBytes(data):
    '''
    Formats the JSON data into the corresponding Python object value
    (could be dict, list, number, string, bool or None).

    '''
    return json.loads(data)
