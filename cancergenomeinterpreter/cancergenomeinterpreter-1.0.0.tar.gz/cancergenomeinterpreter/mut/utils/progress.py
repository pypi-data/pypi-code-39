import datetime
import logging
import os
import threading
import time

from humanize import naturaltime


class ProgressBar(object):
    DELAY = 0.5

    PROGRESS = {
        'default': ["[*       ]", "[ *      ]", "[  *     ]", "[   *    ]", "[    *   ]", "[     *  ]", "[      * ]",
                    "[       *]", "[      * ]", "[     *  ]", "[    *   ]", "[   *    ]", "[  *     ]", "[ *      ]"],
        'web': ["[*       ]\n", "[ *      ]\n", "[  *     ]\n", "[   *    ]\n", "[    *   ]\n", "[     *  ]\n",
                "[      * ]\n", "[       *]\n", "[      * ]\n", "[     *  ]\n", "[    *   ]\n", "[   *    ]\n",
                "[  *     ]\n", "[ *      ]\n"]
    }

    PROGRESS_DONE = {
        'default': "[  done  ]",
        'web': "[  done  ]\n"
    }

    def __init__(self, message="", message_prefix="", theme='default'):
        self.done = False
        self.message = message_prefix + message
        self.message_prefix = message_prefix
        self.debug = logging.getLogger().getEffectiveLevel() == logging.DEBUG
        self.start_time = None
        self.theme = os.getenv('BG_PROGRESS_THEME', theme).strip()
        self.char_color = ""

    def set_message(self, message):
        self.message = self.message_prefix + message
        if self.debug:
            logging.debug(self.message)

    def stop(self):
        self.done = True

        if not self.debug:
            time.sleep(self.DELAY)
        else:
            logging.debug(self.message_prefix + " (" + naturaltime(self.start_time) + ")")

    def start(self):

        self.start_time = datetime.datetime.now()

        if not self.debug:
            # Force logging handlers to flush
            [handler.flush() for handler in logging.getLogger().handlers]
            time.sleep(self.DELAY)
            print(self.char_color + self.PROGRESS[self.theme][0] + ' ' + self.message, end='',
                  flush=True)

            thread = threading.Thread(target=self._run_progress_bar, args=())
            thread.start()

    def _run_progress_bar(self):
        i = 0
        while not self.done:
            print('\r' + self.PROGRESS[self.theme][
                i % len(self.PROGRESS[self.theme])] + ' ' + self.char_color + self.message, end='',
                  flush=True)
            time.sleep(self.DELAY)
            i += 1
        print('\r' + self.PROGRESS_DONE[self.theme] + ' ' + self.char_color + self.message_prefix + " (" + naturaltime(
            self.start_time) + ")", flush=True)
