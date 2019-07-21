#!/usr/bin/env python3
from typing import Callable, Optional
import tkinter


class StartEndApp:
    _start_button: Optional[tkinter.Button]
    window: Optional[tkinter.Tk]

    def __init__(self, start_routine: Callable, end_routine: Callable, window_title='GApp',
                 app_title: Optional[str] = None,
                 always_on_top=True):
        """

        :param window_title: The title of the window
        :param app_title: The title that shows on your body of your app, if omitted, it will be the window title
        :param always_on_top: default is true, set it to false to disable always on top
        :param start_routine: what the start button will do.
        :param end_routine: what the end button will do. It will also close the app. Closing the app by the 'X' button
         will also trigger it first
        """
        self._start = start_routine
        self._started = False
        self._end = end_routine
        self._window_title = window_title
        if app_title is None:
            self._app_title = self._window_title

        self._window = None
        self._start_button = None
        self._always_on_top = always_on_top

    def start_app(self):
        """
        async, starts the app
        """
        window = tkinter.Tk()
        self._window = window

        window.protocol('WM_DELETE_WINDOW', self._destroy_routine)
        window.title(self._window_title)
        window.geometry('300x150')

        app_title_message = tkinter.Message(window, text=self._app_title)

        app_title_message.pack()

        self._start_button = tkinter.Button(window, text="Start", width=25, height=2,
                                            command=self._wrapped_start_routine)
        self._start_button.pack()

        tkinter.Button(window, text="End", width=25, height=2, command=self._end_routine_and_close).pack()

        if self._always_on_top:
            window.attributes('-topmost', True)
            window.update()
        window.mainloop()

    def _wrapped_start_routine(self):
        self._start()
        self._start_button.config(state=tkinter.DISABLED)

    def _end_routine_and_close(self):
        self._end()
        self._window.destroy()

    def _destroy_routine(self):
        self._end()
        self._window.destroy()
