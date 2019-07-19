from abc import ABCMeta, abstractmethod
from prompt_toolkit.layout import ConditionalContainer, Window
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets.toolbars import ValidationToolbar
from prompt_toolkit.layout.controls import FormattedTextControl


class BaseWidget(metaclass=ABCMeta):
    @abstractmethod
    def __pt_container__(self):
        raise NotImplementedError

    def main_control(self):
        return None


class WrapFormattedTextControl(FormattedTextControl):
    def preferred_height(
        self, width, max_available_height, wrap_lines, get_line_prefix
    ):
        content = self.create_content(width, None)
        total = 0
        for i in range(content.line_count):
            total += content.get_height_for_line(i, width, get_line_prefix)

        return total


class QuestionHeaderControl(WrapFormattedTextControl):
    def __init__(self, question):
        self.question = question
        super().__init__(self._build_text, show_cursor=False, focusable=True)

    def _build_text(self):
        tokens = [("class:question.mark", "?"), ("", " ")]
        if isinstance(self.question, list):
            tokens.extend(self.question)
        else:
            tokens.append(("class:question.text", self.question))

        return tokens


class AnswerControl(WrapFormattedTextControl):
    def __init__(self, answer=None):
        self.answer = answer
        super().__init__(self._build_text, show_cursor=False, focusable=False)

    def _build_text(self):
        return [("", " "), ("class:answer.text", self.answer or "")]


class Question(BaseWidget):
    def __init__(self, question):
        self._answer_control = AnswerControl()

        @Condition
        def answered():
            return self.answer is not None

        self.answered = answered

        q = self.build_question()

        self._header_control = QuestionHeaderControl(question)
        widgets = [
            VSplit(
                [
                    Window(
                        self._header_control,
                        wrap_lines=True,
                        dont_extend_height=True,
                        dont_extend_width=True,
                    ),
                    ConditionalContainer(
                        Window(
                            self._answer_control,
                            wrap_lines=True,
                            dont_extend_height=True,
                        ),
                        self.answered,
                    ),
                ]
            )
        ]
        if q is not None:
            widgets.append(ConditionalContainer(q, ~self.answered))

        widgets.extend([ConditionalContainer(ValidationToolbar(), ~self.answered)])

        self._widget = HSplit(widgets, key_bindings=self.key_bindings())

    def build_question(self):
        return

    def __pt_container__(self):
        return self._widget

    @property
    def answer(self):
        return self._answer_control.answer

    def set_answer(self, value, pretty=None):
        if value is None:
            self._answer_control.answer = None
            return

        if pretty is None:
            pretty = default_pretty

        self._answer_control.answer = pretty(value)
        self._handler(value)

    @property
    def question(self):
        return self._header_control.question

    @question.setter
    def question(self, value):
        self._header_control.question = value

    def key_bindings(self):
        return None

    def main_control(self):
        return self._header_control


def default_pretty(v, conv=str):
    return v if isinstance(v, conv) else str(v)
