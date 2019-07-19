from .base import Question
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document


class TextQuestion(Question):
    def __init__(self, question, default=None, **kwargs):
        self._kwargs = kwargs
        buf = Buffer(multiline=False, accept_handler=self._accept, **self._kwargs)
        self._buf_control = BufferControl(buf)
        if default is not None:
            buf.document = Document(default)

        super().__init__(question)

    def main_control(self):
        return self._buf_control

    def build_question(self):
        return Window(self._buf_control, dont_extend_height=True, wrap_lines=True)

    def _accept(self, doc):
        self.set_answer(doc.text)
