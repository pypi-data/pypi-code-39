__name__ = 'astron'
__version__ = '0.1'

import sys, os

sys.path.append('./')
from pre_made import game

game.startGame(splash=True)
