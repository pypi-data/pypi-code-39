from .base import Question
from prompt_toolkit.key_binding import KeyBindings


def defalt_pretty(v):
    return "Yes" if v else "No"


def default_converter(v):
    return True if v.lower() == "y" else False


class YesNoQuestion(Question):
    def __init__(self, question, keys="Yn", pretty=None, converter=None):
        self._keys = keys
        self._pretty = defalt_pretty if pretty is None else pretty
        self._converter = default_converter if converter is None else converter
        self._question_text = ("class:question.text", question)
        self._question_key = ("class::question.key", " [{}]".format(keys))
        super().__init__([self._question_text, self._question_key])

    def key_bindings(self):
        kb = KeyBindings()

        default = None

        for key in self._keys:
            if key.isupper():
                default = key

            @kb.add(key.upper(), eager=True)
            @kb.add(key.lower(), eager=True)
            def _(event, key=key):
                self.question = [self._question_text]
                self.set_answer(self._converter(key), pretty=self._pretty)

        if default is not None:

            @kb.add("enter", eager=True)
            def _(event):
                self.question = [self._question_text]
                self.set_answer(self._converter(default), pretty=self._pretty)

        return kb
