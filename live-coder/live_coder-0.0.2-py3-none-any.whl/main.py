import curses

from ._find_tests import find_test_classes
from ._test_tracker import TestTracker
from ._pick_test_class import pick_a_test_class
from ._constants import INTRO


def _pick_test_class():
    while True:
        test_classes = find_test_classes()
        picked_test_class = pick_a_test_class(test_classes)
        tracker = TestTracker(picked_test_class.methods)
        curses.wrapper(tracker.track, picked_test_class)

def start():
    print(INTRO)
    _pick_test_class()


if __name__ == '__main__':
    start()
