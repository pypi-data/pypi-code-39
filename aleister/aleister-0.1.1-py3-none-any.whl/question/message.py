from prompt_toolkit.layout import Window

from .base import BaseWidget, WrapFormattedTextControl


class Message(BaseWidget):
    def __init__(self, message):
        self._widget = Window(
            WrapFormattedTextControl(message),
            dont_extend_height=True,
            dont_extend_width=True,
        )

    def __pt_container__(self):
        return self._widget
