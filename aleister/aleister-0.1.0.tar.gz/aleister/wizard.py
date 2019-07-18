from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.layout.layout import Layout, Window
from prompt_toolkit.layout.controls import DummyControl
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout
from functools import wraps


class Cancel(Exception):
    pass


class Wizard:
    def __init__(self, questions, key_bindings=None, style=None):
        self._questions_iter = iter(questions)
        self._key_bindings = (
            _get_default_key_bindings() if key_bindings is None else key_bindings
        )
        self._style = _get_default_style() if style is None else style

    def run(self):
        answer = None
        while True:
            try:
                widget = self._questions_iter.send(answer)
            except StopIteration:
                break

            layout = Layout(widget)
            app = Application(
                layout,
                full_screen=False,
                key_bindings=self._key_bindings,
                style=self._style,
            )
            c = widget.main_control()
            if c is not None:
                app.layout.focus(c)
            widget._handler = self._make_handler(app)

            try:
                answer = app.run()
            except Cancel:
                break

    def _make_handler(self, app):
        def handler(answer):
            app.exit(answer)

        return handler


def _get_default_style():
    return Style.from_dict(
        {
            "question.mark": "ansiblue bold",
            "question.text": "bold",
            "question.key": "",
            "answer.text": "ansiyellow bold",
            "choice.selected": "bold",
            "choice.unselected": "",
            "choice.cursor": "ansired bold",
        }
    )


def _get_default_key_bindings():
    k = KeyBindings()

    @k.add("c-c")
    def _(event):
        event.app.exit(exception=Cancel())

    return k


def wizard(style=None, key_bindings=None):
    def wrapped(f):
        @wraps(f)
        def g(*args, **kwargs):
            wiz = Wizard(f(*args, *kwargs), key_bindings=key_bindings, style=style)
            wiz.run()

        return g

    return wrapped
