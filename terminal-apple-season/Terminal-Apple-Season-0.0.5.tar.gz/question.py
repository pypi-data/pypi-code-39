import random
import time
import curses

from apple_season.basket import Basket
from apple_season.apple import Apple
from apple_season.coords import Canvas

def main(stdscr):

    curses.curs_set(1)  # so i can see where the cursor is
    dims = [curses.COLS - 1, curses.LINES - 1]  # pylint: disable=no-member

    stdscr.nodelay(True)
    stdscr.leaveok(True)
    key=""
    stdscr.clear()

    canvas = Canvas(*dims)

    basket = Basket(canvas)

    apples = []
    i = 0

    def finished_apples():
      if len(apples) <= 100:
         return False
      else:
         for apple in apples:
            if not apple.has_fallen:
               return False
         return True

    while not finished_apples():

        if len(apples) <= 100:  # don't make more if there are already 100
            # decide whether or not to create new apple (1/100 chance per frame)
            num = random.randint(0, 100)
            if num == 25:
                apples.append(Apple(canvas))

        try:
            key = stdscr.getkey()
            stdscr.clear()
            
            # pick up keyboard inputs
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

        # render objects - alters canvas to display them
        for apple in apples:
            if apple.has_fallen:
                apple.render()
            else:
                if '.0' not in str(i / 2):  # check if i is even (drop every other frame)
                    apple.fall()
                    apple.render()

        basket.render()

        try:
            stdscr.addstr(canvas.display)
            
        except Exception:
            pass

        stdscr.refresh()
        i += 1
        time.sleep(0.01)

if __name__ == "__main__":
    curses.wrapper(main)
