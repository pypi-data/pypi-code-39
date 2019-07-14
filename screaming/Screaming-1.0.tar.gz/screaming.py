import random
import string

'''

This package gives you an authentic scream string

'''

import yagmail

class Screaming:
    def __init__(self):
        self.s = 's' #no clue this does nothing!

    def getScream(self):
        a,h = 'A','H'
        ah = ''.join( random.choice(a) for i in range(random.randrange(1,19)) )
        ah+=''.join( random.choice(h) for i in range(random.randrange(13,35)) )
        return ah

def scream():
    return Screaming

#USE SETUPTOOLS TO MAKE THIS PROJECT INTO A PACKAGE!!!! WOOOO
