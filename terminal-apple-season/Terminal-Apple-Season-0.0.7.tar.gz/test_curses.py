from os.path import join, dirname
import sys
import time
import logging

cwd = dirname(dirname(__file__))
if cwd not in sys.path:
    sys.path.append(cwd)

import curses

from apple_season.basket import Basket
from apple_season.coords import Canvas


logging.basicConfig(filename='apple.log', level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def main(stdscr):

    curses.curs_set(2)

    canvas = Canvas(curses.COLS - 1, curses.LINES - 1)  # pylint: disable=no-member
    basket = Basket(canvas)

    stdscr.nodelay(True)
    key=""
    stdscr.clear()

    while True:

         try:
            key = stdscr.getkey()

            # quit option
            if str(key) == "q":
                break

            # right arrow
            elif str(key) == "KEY_RIGHT":
                basket.move('right')

            # left arrow
            elif str(key) == "KEY_LEFT":
                basket.move('left')

         except Exception:
            pass

         basket.render()
         stdscr.clear()
         stdscr.addstr(canvas.display)
         logging.debug(f'cursor position: {str(stdscr.getyx())}')
         stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)