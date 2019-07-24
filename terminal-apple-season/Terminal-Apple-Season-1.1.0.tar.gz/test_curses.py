from os.path import join, dirname, abspath
import sys
import time
import curses

from termcolor import colored

cwd = dirname(abspath(__file__))
if cwd not in sys.path:
    sys.path.append(cwd)

from apple_season.basket import Basket
from apple_season.coords import Canvas


def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    stdscr.clear()

    if curses.has_colors():
        while True:
            stdscr.addstr('')
            stdscr.refresh()
            stdscr.clear()
    else:
        while True:
            stdscr.addstr('false')
            stdscr.refresh()
            stdscr.clear()


if __name__ == "__main__":
    curses.wrapper(main)
    # playsound(join(cwd, 'apple_season/caught.mp3'))