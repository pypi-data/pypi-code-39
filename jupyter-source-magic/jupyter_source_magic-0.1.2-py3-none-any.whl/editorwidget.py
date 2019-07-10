import re

from jupyter_interval_widget import Interval
from ipywidgets.widgets import Button, Output, HBox, VBox
from IPython.display import display, clear_output, Javascript
from IPython.utils.py3compat import input

from .haltexecution import HaltExecution

MAGICS_REGEX = r"^((\n*(%%.+)\n)+)"

class EditorWidget(VBox):
    def __init__(self, file_manager, shell, line, cell, path, no_eval, \
                 conflict_resolution_strategy, pooling_rate=None, debug=False):
        super(EditorWidget, self).__init__()
        self.file_manager = file_manager
        self.shell = shell
        self.line = line
        self.cell = cell
        self.path = path
        self.no_eval = no_eval
        self.conflict_resolution_strategy = conflict_resolution_strategy
        self.pooling_rate =  pooling_rate if pooling_rate > 0 else None
        self.debug = debug
        self.cell_magics = re.match(MAGICS_REGEX, "%%source " + self.line + "\n" + self.cell).group(1)
        self.cell_content_to_save = re.sub(MAGICS_REGEX, "", self.cell) + "\n"
        self.status_output = Output()
        self.file_change_monitor = Interval(value=self.pooling_rate)
        self.file_change_monitor.on_tick(lambda widget: self.check_external_modification())
        self.overwrite_button = Button(description="Overwrite", button_style="danger", layout={ "display": "none" })
        self.overwrite_button.on_click(lambda widget: self.save_file_and_run_cell())
        self.refresh_button = Button(description="Refresh", button_style="danger", layout={ "display": "none" })
        self.refresh_button.on_click(lambda widget: self.refresh_cell())
        self.cell_output = Output()

        self.file_status_widgets = HBox(children=(self.status_output, self.overwrite_button, self.refresh_button))
        if self.pooling_rate:
            self.file_status_widgets.children += (self.file_change_monitor,)

        self.children = (self.file_status_widgets, self.cell_output)
        if self.debug:
            self.debug_output = Output()
            self.children = (self.debug_output,) +self.children

        self.state = "Cell was just run"

    def eval_cell(self):
        if self.no_eval:
            return
        with self.cell_output:
            clear_output(wait=True)
            self.shell.run_cell(self.cell, store_history=False)

    def save_file_and_run_cell(self):
        self.file_manager.save(self.path, self.cell_content_to_save)
        self.eval_cell()

    def refresh_cell(self):
        self.file_manager.manage(self.path, self.file_manager.read(self.path))
        js = """
            var cmd = "import os; import sys; f = open('%s', 'r'); sys.stdout.write(f.read()); f.close()";
            function handle_output(msg) {
                var cell_magic_lines = IPython.notebook.get_selected_cell().get_text().match(/^(%%%%.*\\n)*/)[0]
                var file_content = msg.content.text;
                IPython.notebook.get_selected_cell().set_text(cell_magic_lines + file_content);
            }
            var callback = {'output': handle_output};
            IPython.notebook.kernel.execute(cmd, {iopub: callback}, {silent: false});
        """
        clear_output(wait=True)
        display(self)
        display(Javascript(js % (self.path,)))


    def display_status(self, status):
        self.status_output.layout = {}
        with self.status_output:
            clear_output(wait=True)
            display(status)

    def display_debug(self, message):
        from datetime import datetime
        with self.debug_output:
            clear_output(wait=True)
            display(message + " " + str(datetime.now()))

    def show_button(self, button):
        button.layout = {}

    def prompt_conflict_resolution(self, state):
        if state == "File was deleted by another process":
            answers = {'1': 'Keep Cell Contents and Continue Execution', \
                       '2': 'Overwrite File and Continue Execution', \
                       '3': 'Abort'}
        else:
            answers = {'1': 'Keep Cell Contents and Continue Execution', \
                       '2': 'Overwrite File and Continue Execution', \
                       '3': 'Halt Execution and Refresh Cell Contents', \
                       '4': 'Abort'}

        prompt_text = state + "\n\n" + "\n".join(['%s: %s' % (key, value) for (key, value) in sorted(answers.items())]) + "\n\n"

        ans = None

        while ans not in answers.keys():
            ans = input(prompt_text + ' ')

        clear_output(wait=True)
        display(self)

        return answers[ans]

    def display_conflict_resolution(self):
        self.display_status(self.state)
        if self.state != "File was deleted by another process":
            self.show_button(self.refresh_button)
        self.show_button(self.overwrite_button)

    def process_cell_execution(self):
        state = self.file_manager.get_initial_state(self.path, self.cell_content_to_save)
        self.state = state

        if self.debug: self.display_debug(self.state)

        if self.state == "In sync, new content":
            self.save_file_and_run_cell()
        elif self.state == "In sync, unchanged content":
            self.eval_cell()
        elif self.state == "New file":
            self.save_file_and_run_cell()
        elif self.state == "File exists with same contents":
            self.file_manager.manage(self.path, self.cell_content_to_save)
            self.eval_cell()
        elif self.state in ("File exists with different contents", \
                            "File was changed by another process", \
                            "File was deleted by another process"):
            if self.conflict_resolution_strategy == "Prompt":
                resolution = self.prompt_conflict_resolution(self.state)
            else:
                resolution = self.conflict_resolution_strategy
            if resolution == "Keep Cell Contents and Continue Execution":
                self.eval_cell()
                self.display_conflict_resolution()
            elif resolution == "Overwrite File and Continue Execution":
                self.file_manager.save(self.path, self.cell_content_to_save)
                self.eval_cell()
            elif resolution == "Halt Execution and Refresh Cell Contents":
                self.shell.set_next_input(self.cell_magics + self.file_manager.read(self.path), replace=True)
                raise HaltExecution
            elif resolution == "Abort":
                self.display_conflict_resolution()
                raise HaltExecution

    def check_external_modification(self):
        state = self.file_manager.get_state_change(self.path, self.cell_content_to_save)
        if state == None or state == self.state:
            return
        self.state = state

        if self.debug: self.display_debug(self.state)

        for button in (self.overwrite_button, self.refresh_button):
            button.layout = { "display": "none" }
        self.status_output.layout = { "display": "none" }

        if state == "In sync, unchanged content":
            pass
        if state in ("File was changed by another process", \
                     "File was deleted by another process", \
                     "File exists at this path"):
            self.display_conflict_resolution()
