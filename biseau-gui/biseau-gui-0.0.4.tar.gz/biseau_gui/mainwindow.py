"""Empty docstring"""

import sys
import biseau as bs
import clyngor
import pkg_resources
from collections import defaultdict
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


from .imageviewer import ImageViewer
from .dotviewer import DotViewer
from .aspviewer import ASPViewer
from .modelsviewer import ModelsViewer
from .logwidget import LogWidget
from .tuto import TutorialViewer
from .scriptlistwidget import ScriptListWidget, ScriptRole
from .scripteditor import ScriptEditor
from .scriptbrowser import ScriptBrowserDialog
from .script_exporter import ScriptExporterDialog


import time


class MainWindow(QMainWindow):
    def __init__(self, parent=None, default_script:str=None):
        super(MainWindow, self).__init__(parent)
        self.tab_widget = QTabWidget()
        self.log_widget = LogWidget()
        self.script_list_widget = ScriptListWidget()
        self._dock_of_script = defaultdict(list)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.log_widget)
        self.splitter.setStretchFactor(0, 9)
        self.splitter.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter)

        self._enable_cxt_viewer = True
        self._setup_main_tabs()

        # Build left script list view
        scripts_dock = QDockWidget()
        scripts_dock.setWindowTitle("Scripts")
        scripts_dock.setWidget(self.script_list_widget)
        scripts_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, scripts_dock)

        # setup toolbar and menubar
        self.setup_action()

        # give focus on script editor
        self.script_list_widget.view.itemClicked.connect(
            lambda item: self.set_focus_on_editor(item.data(ScriptRole))
        )

        # Autocompile if script is checked
        self.script_list_widget.view.itemChanged.connect(self.auto_run)

        # (un)comment this to load working scripts
        # self.add_script_from_file("scripts/test_option_types.py")
        self.first_time = True
        if default_script == 'simple':
            self.add_default_script()
        elif default_script == 'gene':
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/raw_data.lp"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/compute_score.py"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/render_interactions.json"))
        elif default_script == 'init':
            script = self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/context.py"))
            script.options_values['context_file'] = pkg_resources.resource_filename(__name__, "embedded_contexts/human.cxt")
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/fca_concepts.lp"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/fca_lattice.lp"))
        elif default_script == 'FCA':
            script = self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/context.py"))
            script.options_values['context_file'] = pkg_resources.resource_filename(__name__, "embedded_contexts/human.cxt")
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/build_concepts.py"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/build_galois_lattice.json"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/show_galois_lattice.py"))
        elif default_script == 'record':
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/record-example.lp"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/record.py"))
        elif default_script == 'tuto-ASP-basics':
            target_tuto = 'ASP basics'
            self.run_tutorial(target_tuto, TutorialViewer.tutorials[target_tuto])
        else:
            print('No example loaded. Available examples: simple, gene.')
        self.run()

    def _setup_main_tabs(self):
        "Destroy existing tabs, rebuild them"
        # already exists: lets save some things
        saved_asp = self.asp_viewer.get_asp() if self.tab_widget.count() else None
        # remove everything
        while self.tab_widget.count():
            self.tab_widget.removeTab(self.tab_widget.currentIndex())

        # create the viewers
        self.image_viewer = ImageViewer()
        self.dot_viewer = DotViewer(self.image_viewer)
        if self._enable_cxt_viewer:
            self.cxt_viewer = ModelsViewer(self.dot_viewer)
            self.asp_viewer = ASPViewer(self.cxt_viewer)
        else:  # don't add the supplementary step
            self.asp_viewer = ASPViewer(self.dot_viewer)

        self.add_central_view(self.image_viewer)
        self.add_central_view(self.dot_viewer)
        if self._enable_cxt_viewer:  self.add_central_view(self.cxt_viewer)
        self.add_central_view(self.asp_viewer)
        self.tab_widget.setCurrentWidget(self.image_viewer)

        # in cases things has been saved…
        if saved_asp:
            self.asp_viewer.set_asp(saved_asp)

    def focus_central_tab(self, name:str):
        "Change the tab focused on the central area"
        for elem in (self.image_viewer, self.dot_viewer, self.cxt_viewer, self.asp_viewer):
            if elem.windowTitle().lower() == name.lower():
                self.tab_widget.setCurrentWidget(elem)
                break
        else:
            raise ValueError(f"Tab of name '{name}' wasn't matched by existing tab")


    def setup_action(self):
        # Setup menu bar
        self.tool_bar = self.addToolBar("main")
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        add_script_file_action = self.tool_bar.addAction(
            QIcon.fromTheme("list-add"), "Add script", self.open_script
        )
        add_script_action = self.tool_bar.addAction(
            QIcon.fromTheme("list-add"), "Add default script", self.add_default_script
        )

        # Create Add Menu
        add_menu = QMenu("Add script ...")
        add_menu.addAction(add_script_file_action)
        add_menu.addAction(add_script_action)

        run_action = self.tool_bar.addAction(
            QIcon.fromTheme("media-playback-start"), "Run", self.run
        )
        stop_action = self.tool_bar.addAction(
            QIcon.fromTheme("media-playback-stop"), "Stop", self.stop
        )
        clean_action = self.tool_bar.addAction(
            QIcon.fromTheme("edit-clear"), "Clean Cache", self.clean_cache
        )
        self.auto_run_action = self.tool_bar.addAction(
            QIcon.fromTheme("view-refresh"), "Auto compile"
        )
        export_action = self.tool_bar.addAction(
            QIcon.fromTheme("export"), "Export", self.export_scripts
        )

        add_script_file_action.setShortcut(QKeySequence.Open)
        run_action.setShortcut(Qt.CTRL + Qt.Key_R)
        self.auto_run_action.setCheckable(True)
        self.auto_run_action.triggered.connect(self.set_auto_compile)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addMenu(add_menu)
        file_menu.addSeparator()
        file_menu.addAction("&Quit", self.close)
        self.view_menu = self.menuBar().addMenu("&View")
        self.view_menu.addAction('Toogle Model view', self.toggle_model_view)

        help_menu = self.menuBar().addMenu("&Tutorials")
        for name, tutorial in TutorialViewer.tutorials.items():
            help_menu.addAction(name, lambda: self.run_tutorial(name, tutorial))


        help_menu = self.menuBar().addMenu("&About")
        help_menu.addAction("About Qt", qApp.aboutQt)

    def add_central_view(self, widget: QWidget):

        self.tab_widget.addTab(widget, widget.windowTitle())

    def open_script(self):
        "Prompt user about a file, try to load a script from it"

        dialog = ScriptBrowserDialog()
        if dialog.exec_():
            for script in dialog.get_scripts():
                self.add_script(script)

    def add_script_from_file(self, filename):
        """add one script into the app. Create list item and dock"""
        # TODO: we should be able to load any script in the file, not only the first
        script = next(bs.module_loader.build_scripts_from_file(filename), None)
        self.add_script(script)
        return script

    def add_script(self, script: bs.Script):
        """add one script into the app. Create list item and dock"""
        # TODO: we should be able to load any script in the file, not only the first
        if not script:
            return
        self.script_list_widget.add_script(script)
        # create dock script editor
        editor = ScriptEditor(script)
        dock = self._add_as_dock(editor, script.name)
        editor.changed.connect(self.auto_run)
        self._dock_of_script[script].append(dock)  # enables to delete it when removing the script
        self.auto_run()

    def _add_as_dock(self, widget:QWidget, name:str) -> QDockWidget:
        "Add given widget as a dock  on the right of the main window"
        dock = QDockWidget()
        dock.setWindowTitle(name)
        dock.setWidget(widget)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.view_menu.addAction(dock.toggleViewAction())
        return dock

    def add_default_script(self):
        if self.first_time:
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/default.lp"))
        else:
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/blank.lp"))
        self.first_time = False

    def update_scripts_from_editors(self):
        """ call ScriptEditor.update() on each editor """
        dockWidgets = self.findChildren(QDockWidget)
        for dock in dockWidgets:
            if type(dock.widget()) == ScriptEditor:
                dock.widget().update_script()

    def docks_from_script(self, script: bs.Script):
        """ TODO : dict should be better """
        return self._dock_of_script.get(script, ())

    def set_focus_on_editor(self, script: bs.Script):
        for dock in self.docks_from_script(script):
            # dock.widget().edit_widget.activateWindow()
            dock.widget().edit_widget.setFocus()
            # dock.widget().edit_widget.setFocusPolicy(Qt.StrongFocus)
            # dock.widget().edit_widget.raise_()

    def delete_docks_of_script(self, script: bs.Script):
        for dock in self.docks_from_script(script):
            self.removeDockWidget(dock)


    def run(self):
        """ Run biseau and display the dot file """

        # freeze gui
        self.script_list_widget.setDisabled(True)

        # Update script from editors
        self.update_scripts_from_editors()

        # Run main loop
        try:
            context = ""
            scripts = self.script_list_widget.get_scripts()
            for index, (context, duration) in enumerate(bs.core.yield_run(scripts)):
                self.script_list_widget.set_item_duration(index, duration)
                self.script_list_widget.set_current_script(scripts[index])
                qApp.processEvents()
            self.set_asp(context)
        except clyngor.utils.ASPSyntaxError as e:
            self.log_widget.add_message(str(e))
        else:  # no error, let's empty the log widget
            self.log_widget.erase_all('Successful execution')
        self.script_list_widget.setEnabled(True)

    def auto_run(self):
        if self.auto_run_action.isChecked():
            self.run()

    def stop(self):
        ... # TODO: kill action_run thread

    def clean_cache(self):
        ... # TODO : self.scripting_widget.clear_cache()

    def set_auto_compile(self, active: bool):
        ... # TODO: change button style

    def export_scripts(self):
        "Export current scripts in a single executable file"
        scripts = self.script_list_widget.get_scripts()
        dialog = ScriptExporterDialog(self, scripts)
        dialog.exec_()

    def toggle_model_view(self):
        self._enable_cxt_viewer = not self._enable_cxt_viewer
        self._setup_main_tabs()



    def set_asp(self, context:str):
        "Send dot file to the dot viewer for compilation"
        self.asp_viewer.set_asp(context)

    @staticmethod
    def start_gui(*args, **kwargs):
        app = QApplication(sys.argv)
        w = MainWindow(*args, **kwargs)
        w.showMaximized()
        return app.exec_()

    def run_tutorial(self, name:str, sequence, step=0):
        "Remove all scripts, starts the Tutorial view"
        self.tab_widget.setCurrentWidget(self.asp_viewer)  # show the asp code
        self.script_list_widget.remove_all_scripts()
        tuto_interface = TutorialViewer(self, sequence=sequence, step=step, name_template=name + ' {step}')
        self.script_list_widget.add_script(tuto_interface)
        dock = self._add_as_dock(tuto_interface, name)
        tuto_interface.name_changed.connect(dock.setWindowTitle)

        self._dock_of_script[tuto_interface].append(dock)  # enables to delete it when removing the script
        self.auto_run()


