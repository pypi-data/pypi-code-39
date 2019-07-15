'''
    Test for removing random whitespace
'''
import re

def rmspace(string):
    '''
        Remove arbitrary whitespace
    '''
    # remove space before and after string and all but one in the middle
    return re.sub(' +', ' ',string.strip())


a    =   ['1    2','    3 4 ',' 5        6   ']

for i in a:
    rmspace(i)