from .base import Question
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout import HSplit, VSplit, Window
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters.app import has_focus
from prompt_toolkit.document import Document


class ChoiceCandidatesControl(FormattedTextControl):
    def __init__(self, candidates, default=0):
        self._candidates = candidates
        self.selected_item = default
        super().__init__(self._build_text, show_cursor=False, focusable=True)

    def _build_text(self):
        tokens = []
        for i, c in enumerate(self._candidates):
            if i == self.selected_item:
                tokens.extend(
                    [("class:choice.cursor", "❯ "), ("class:choice.selected", c)]
                )
            else:
                tokens.extend([("", "  "), ("class:choice.unselected", c)])
            tokens.append(("", "\n"))

        tokens.pop()
        return tokens


class ChoiceOtherLabelControl(FormattedTextControl):
    def __init__(self, selected=False, label=None):
        self.selected = selected
        self.label = "other" if label is None else label
        super().__init__(self._build_text, show_cursor=False, focusable=False)

    def _build_text(self):
        if self.selected:
            return [
                ("class:choice.cursor", "❯ "),
                ("class:choice.selected", self.label),
                ("class:choice.selected", ": "),
            ]
        else:
            return [
                ("", "  "),
                ("class:choice.unselected", self.label),
                ("class:choice.unselected", ": "),
            ]


class ChoiceQuestion(Question):
    def __init__(self, question, candidates, other=False, default=None, **kwargs):
        self._candidates = candidates

        self._other = other
        self._selected, other_value = self._get_default_selected(default)

        self._candidate_control = ChoiceCandidatesControl(candidates, self._selected)
        if self.has_other:
            buf = Buffer(accept_handler=self._buffer_handler, multiline=False, **kwargs)
            buf.document = Document(other_value)
            self._other_value_control = BufferControl(buf)
            self._other_label_control = ChoiceOtherLabelControl(
                self.other_selected,
                self._other if isinstance(self._other, str) else None,
            )

        super().__init__(question)

    def build_question(self):
        w = [Window(self._candidate_control, dont_extend_height=True)]
        if self.has_other:
            w.append(
                VSplit(
                    [
                        Window(
                            self._other_label_control,
                            dont_extend_width=True,
                            dont_extend_height=True,
                        ),
                        Window(self._other_value_control, dont_extend_height=True),
                    ]
                )
            )

        return HSplit(w, key_bindings=self._get_key_bindings())

    def _get_key_bindings(self):
        kb = KeyBindings()

        on_sel = ~has_focus(self._other_value_control) if self.has_other else True

        @kb.add("j", filter=on_sel)
        @kb.add("down", filter=on_sel)
        @kb.add("c-n", filter=on_sel)
        def _(event):
            self.move_cursor(1)

        @kb.add("k", filter=on_sel)
        @kb.add("up", filter=on_sel)
        @kb.add("c-p", filter=on_sel)
        def _(event):
            self.move_cursor(-1)

        @kb.add("enter", filter=on_sel)
        def _(event):
            if self.other_selected:
                return event.app.layout.focus(self._other_value_control)

            self.set_answer(self._candidates[self._selected])

        return kb

    def _buffer_handler(self, doc):
        self.set_answer(doc.text)

    def _get_default_selected(self, default):
        if default is None:
            return 0, ""

        if not self.has_other:
            return self._candidates.index(default), ""

        try:
            return self._candidates.index(default), ""
        except ValueError:
            return len(self._candidates), default

    @property
    def other_selected(self):
        return self._selected == len(self._candidates)

    @property
    def has_other(self):
        return self._other is not None and self._other is not False

    @property
    def num_candidates(self):
        return len(self._candidates) + (1 if self.has_other else 0)

    def move_cursor(self, d):
        self._selected = (self._selected + d) % self.num_candidates
        if self.has_other:
            if self.other_selected:
                self._candidate_control.selected_item = None
                self._other_label_control.selected = True
            else:
                self._candidate_control.selected_item = self._selected
                self._other_label_control.selected = False
        else:
            self._candidate_control.selected_item = self._selected

    def main_control(self):
        return self._candidate_control
