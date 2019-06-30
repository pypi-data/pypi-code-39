"""Definition of the TutorialView Widget"""


import time
import random
import inspect
import clyngor
import threading
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


def run_player(code:str) -> [(float, str)]:
    "Yield time to wait and string to print"
    for line in code.splitlines(False):
        if line.startswith('$'):  # it's a command !
            command, *args = line[1:].strip().split(' ')
            if command == 'pause':
                assert len(args) in {0, 1}, args
                yield float(args[0] if args else 1.), ''
            else:
                yield command, args
            continue  # nothing else to do
        elif '%' in line:
            code, comment = line.split('%', 1)
            comment = '%' + comment
        elif not line.strip():  # empty line
            code, comment = '', ''
        else:
            code, comment = line, ''
        for char in code:  # code must be written slowly, organically
            yield 0.08 * random.randint(1, 3), char
        for char in comment:  # code must be written as if someone spoke it
            yield 0.02, char
        yield (0.1 if comment and comment[-1] != '.' else 0.5), '\n'  # finish by newline


class TutorialViewer(QWidget):
    """This widget is to be integrated as any script viewer."""
    name_changed = Signal(str)

    def __init__(self, mainwindow, sequence, step:int=0, name_template:str='Tuto {step}'):
        super().__init__()
        self.mainwindow = mainwindow
        self.name_template = name_template
        self.atoms_validator = None  # used during exercises
        self.setLayout(QVBoxLayout())
        self.sequence, self.step = sequence, step
        self.set_name()
        self._build_interface()
        # emulation of script behavior
        self.description, self.input_mode, self._run_on = '', str, lambda *a, **k: self._run()
        self.options, self.options_values, self.erase_context = (), {}, True
        self.aggregate = False
        self.thread_interactive = None
        self._restart()

    def _build_interface(self, first_step=False, last_step=False):
        self.edit_widget = QTextEdit()
        self.edit_widget.setFont('Monospace')

        ACTIONS = {
            'prev': ('<', "Go back to the previous step of the tutorial"),
            'run': ('Run', "Run the code, updating the general view"),
            'validate': ('Validate', "Verify if the ASP code answers to the question (if a question has been asked)"),
            'reset': ('Reset', "Reset the code to initial state"),
            'next': ('>', "Go to the next step of the tutorial")
        }
        self._buttons = {}
        but_layout = QHBoxLayout()
        for action, (name, tooltip) in ACTIONS.items():
            button = QPushButton(name, clicked=getattr(self, '_' + action))
            button.setToolTip(tooltip)
            but_layout.addWidget(button)
            self._buttons[action] = button

        # integrate everything
        self.layout().addWidget(self.edit_widget)
        self.layout().addLayout(but_layout)


    def _update_interface(self):
        self.set_asp('')
        # setup buttons
        for action, button in self._buttons.items():
            first_step = self.step == 0
            last_step = (self.step+1) == len(self.sequence)
            button.setDisabled(any((
                (action == 'prev' and first_step),
                (action == 'next' and last_step),
                (action == 'validate' and not self.isExercise),
            )))
        self._color_button('next', None)
        self._color_button('validate', None)
        self._buttons['validate'].setText('Validate')


    def _destroy_interface(self):
        while self.layout().count():
            widget = self.layout().takeAt(0).widget()
            widget.setParent(None)
            widget.deleteLater()


    def set_name(self):
        "Compute current name, emit associated signal"
        self.name = self.name_template.format(step=self.step+1)
        self.name_changed.emit(self.name)

    def set_asp(self, source, compile_and_send=True):
        self.edit_widget.setPlainText(source)
        if compile_and_send:
            self.mainwindow.set_asp(self.get_asp())

    def get_asp(self):
        return self.edit_widget.toPlainText()

    def _run(self):  self.set_asp(self.get_asp()) ; return self.get_asp()
    def _validate(self):
        if self.atoms_validator(self.get_asp()):
            self._buttons['validate'].setText('Validated !')
            self._color_button('validate', 'green')
            self._color_button('next', 'green')
        else:
            self._color_button('validate', 'red')

    def _prev(self):
        self.step -= 1
        self._restart()

    def _next(self):
        "If currently writing text, instantly finish the writing. Else, pass to next stage of tutorial."
        if self.thread_interactive and not self.thread_interactive.isFinished():
            self.thread_interactive.do_waits = False
        else:
            self.step += 1
            self._restart()

    def _reset(self):
        self._restart(write_slowly=False)

    def _restart(self, write_slowly:bool=True):
        try:
            self.sequence[self.step]
        except IndexError as err:
            raise err  # TODO: need an error message
        code, self.atoms_validator = self.stage_code()
        self.set_name()
        self._stop()
        self._update_interface()
        self.edit_widget.setReadOnly(True)
        self.thread_interactive = TutorialPrompter(code, do_waits=write_slowly)
        self.thread_interactive.text_to_be_added.connect(self.add_text)
        self.thread_interactive.command_to_be_run.connect(self.execute_tuto_command)
        self.thread_interactive.start()
        self.thread_interactive.finished.connect(lambda: self.edit_widget.setReadOnly(False))
        if not write_slowly:
            while not thread.isFinished():  thread.wait(10)
            assert thread.isFinished()

    def _stop(self):
        if self.thread_interactive is not None:
            self.thread_interactive.request_stop()
            self.thread_interactive.finished.disconnect()
            self.thread_interactive.text_to_be_added.disconnect()
            self.thread_interactive.command_to_be_run.disconnect()
            while not self.thread_interactive.isFinished(): self.thread_interactive.wait(10)
            self.thread_interactive.deleteLater()
            self.thread_interactive = None
        self.edit_widget.setReadOnly(False)

    def add_text(self, text:str):
        """Add given text to the editor"""
        self.set_asp(self.get_asp() + text, compile_and_send=False)

    def stage_code(self) -> str:
        stage = self.sequence[self.step]
        if isinstance(stage, str):
            return stage, None
        elif isinstance(stage, tuple) and len(stage) == 2 and isinstance(stage[0], str) and callable(stage[1]):
            return stage[0], make_validator_from_object(stage[1])
        else:
            NotImplementedError(f"Behavior for tuto step of type {type(stage)}")

    @property
    def isExercise(self) -> bool:
        return self.atoms_validator is not None

    def execute_tuto_command(self, command, args):
        if command == 'focus':
            assert len(args) == 1, args
            self.mainwindow.focus_central_tab(*args)
        elif command == 'run':
            assert len(args) == 0, args
            self.mainwindow.run()
        elif command == 'wait':
            ... # TODO make it wait for a mouse click or something like that
        elif command == 'end':
            self._color_button('next', 'green')
        else:
            raise ValueError(f"Unknow tutorial command: {command}, with args {args}")

    def _color_button(self, name, color):
        if color:
            self._buttons[name].setStyleSheet(f'background-color: {color}')
        else:
            self._buttons[name].setStyleSheet('')


class TutorialPrompter(QThread):
    """Thread that put the given text in the given QTextEdit, but very slowly,
    so that user sees it written.

    """
    text_to_be_added = Signal(str)
    command_to_be_run = Signal(str, list)

    def __init__(self, text:str, do_waits:bool=True):
        super().__init__()
        self.text = text
        self.do_waits = do_waits
        self.must_stop = False  # If True, the thread will stop ASAP

    def request_stop(self):
        self.do_waits = False
        self.must_stop = True

    def run(self):
        "Slowly add the text to the text widget"
        if isinstance(self.text, str):  # it's a pure player
            runner = run_player(self.text)
        else:
            NotImplementedError(f"Behavior for tuto step of type {type(self.text)}")
        for waitfor, text in runner:
            if isinstance(waitfor, str):  # it's a command ! (and text are args)
                self.command_to_be_run.emit(waitfor, text)
            else:  # it's text !
                waitfor += time.time()  # make it a target
                while waitfor > time.time() and self.do_waits:
                    time.sleep(0.01)
                    if self.must_stop:  break
                self.text_to_be_added.emit(text)
        self.exit()


def make_validator_from_object(obj:callable or str or tuple) -> callable:
    """Decorator uniformizing the given object into a function ASP code -> bool.

    Functions must have only one argument, being either:
    - model:any, where one call is issued for each model, and at least one must return True to pass validation
    - model:all, idem, but all of them has to return True
    - models, all models are given to the function

    If obj is a string or a tuple of string, all the models must have the
    described atoms.

    """
    raise_err = False
    per_model = True
    quantifier = all
    atom_as_string = False
    if callable(obj):
        argspec = inspect.getfullargspec(obj)
        if len(argspec.args) == 1 and argspec.args[0] == 'model' and argspec.annotations.get('model') is all:
            per_model = True
            quantifier = all
        elif len(argspec.args) == 1 and argspec.args[0] == 'model':
            per_model = True
            quantifier = any
        elif len(argspec.args) == 1 and argspec.args[0] == 'models':
            per_model = False
            quantifier = any  # whatever, there will be only one call
        else:
            raise_err = True
        func = obj
    elif isinstance(obj, str):
        per_model = True
        quantifier = all
        atom_as_string = True
        def func(model:all):
            return obj in model
    elif isinstance(obj, tuple) and all(isinstance(sub, str) for sub in obj):
        per_model = True
        quantifier = all
        atom_as_string = True
        def func(model:all):
            return all(sub in model for sub in obj)
    else:
        raise_err = True
    if raise_err:
        raise NotImplemetedError(f"Validator {obj} of type {type(obj)} is not handled")

    def validator(asp_code:str) -> bool:
        models = clyngor.solve(inline=asp_code)
        if atom_as_string:
            models.atom_as_string
        else:
            models.by_arity
        try:
            if per_model:
                return quantifier(func(model) for model in models)
            else:
                return bool(func(models))
        except clyngor.ASPSyntaxError:
            return False
    return validator

