"""Empty docstring"""

import sys
import biseau as bs
import clyngor
import pkg_resources
from collections import defaultdict
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


from . import qtutils
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
from .output_exporter import OutputExporterDialog


import time


class ComputationWorker(QObject):
    """Thread that compile the context to ASP, by running each script in order"""
    ASPGenerated = Signal(str)

    def __init__(self, scripts, logger, script_list_widget):
        super().__init__(parent=None)
        self.must_stop = False  # If True, the thread will stop ASAP
        self.scripts = scripts
        self.logger = logger
        self.script_list_widget = script_list_widget
        self.final_asp_context = None

    def request_stop(self):
        self.must_stop = True

    @Slot()
    def run(self):
        loop = self.loop()
        while not self.must_stop:
            if next(loop, None) is None: break

    def loop(self):
        context = ''
        scripts = self.scripts
        try:
            for index, (context, duration) in enumerate(bs.core.yield_run(scripts)):
                self.script_list_widget.set_item_duration(index, duration)
                self.script_list_widget.set_current_script(scripts[index])
                qApp.processEvents()
                yield True
            self.ASPGenerated.emit(context)
        except clyngor.utils.ASPSyntaxError as e:
            self.logger.add_message(str(e))
        else:  # no error, let's empty the log widget
            self.logger.erase_all('Successful execution')


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

        # Build left script list view
        scripts_dock = QDockWidget()
        scripts_dock.setWindowTitle("Scripts")
        scripts_dock.setWidget(self.script_list_widget)
        scripts_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, scripts_dock)

        # setup toolbar and menubar
        self.setup_action()

        # setup the central tabs
        self._setup_main_tabs()
        # give focus on script editor
        self.script_list_widget.view.itemClicked.connect(
            lambda item: self.set_focus_on_editor(item.data(ScriptRole))
        )

        # Autocompile if script is checked
        self.script_list_widget.view.itemChanged.connect(self.auto_run)

        # (un)comment this to load working scripts
        # self.add_script_from_file("scripts/test_option_types.py")
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
        elif default_script == 'metabolic-network':
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_contexts/metabolic-network-ex1.lp"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/metabolic_network_seed_search.py"))
            self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/render-metabolic-network.lp"))
        elif default_script == 'tuto-ASP-basics':
            target_tuto = 'ASP basics'
            self.run_tutorial(target_tuto, *TutorialViewer.tutorials[target_tuto])
        elif default_script == 'tuto-pyscript-basics':
            target_tuto = 'Python scripting of biseau: a primer'
            self.run_tutorial(target_tuto, *TutorialViewer.tutorials[target_tuto])

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
        self.image_viewer = ImageViewer(self, dot_engine_getter=self.current_dot_engine)
        self.dot_viewer = DotViewer(self.image_viewer)
        if self._enable_cxt_viewer:
            self.cxt_viewer = ModelsViewer(self.dot_viewer)
            self.asp_viewer = ASPViewer(self.cxt_viewer)
        else:  # don't add the supplementary step
            self.asp_viewer = ASPViewer(self.dot_viewer)

        # connect signals between views
        self.image_viewer.ToggleMultishotMode.connect(self.asp_viewer.toggle_multishot_mode)

        add = lambda wid: self.tab_widget.addTab(wid, wid.windowTitle())
        add(self.image_viewer)
        add(self.dot_viewer)
        if self._enable_cxt_viewer:  add(self.cxt_viewer)
        add(self.asp_viewer)
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

        # Create the Add script button and its submenu
        menubutton_add_script, _ = qtutils.add_menubutton(self, "Add script", on_clicked=self.open_script, icon=QIcon.fromTheme("list-add"), toolbar=self.tool_bar, menuitems=(
            ("from file", self.open_script),
            ("default", self.add_default_script),
            ("blank", self.add_blank_script),
        ))
        # Create the 'dot engine' button and its submenu
        menubutton_run, group = qtutils.add_menubutton(self, "Run", on_clicked=self.run, icon=QIcon.fromTheme("media-playback-start"), toolbar=self.tool_bar, menuitems=(
            (name,) for name in ('dot', 'neato', 'circo')
        ), menu_is_choice=True, default='dot')
        group.triggered.connect(self.run)
        self.menubutton_dot_engine_group = group

        # Create other actions
        stop_action = self.tool_bar.addAction(
            QIcon.fromTheme("media-playback-stop"), "Stop", self.stop
        )
        clean_action = self.tool_bar.addAction(
            QIcon.fromTheme("edit-clear"), "Clean Cache", self.clean_cache
        )
        self.auto_run_action = self.tool_bar.addAction(
            QIcon.fromTheme("view-refresh"), "Auto compile"
        )

        # Create the 'export' button and its submenu
        menubutton_export, _ = qtutils.add_menubutton(self, "Export", on_clicked=self.export_images, icon=QIcon.fromTheme("export"), toolbar=self.tool_bar, menuitems=(
            ("outputs", self.export_images),
            ("scripts", self.export_scripts),
        ))

        menubutton_add_script.setShortcut(QKeySequence.Open)
        menubutton_run.setShortcut(Qt.CTRL + Qt.Key_R)
        self.auto_run_action.setCheckable(True)
        self.auto_run_action.triggered.connect(self.set_auto_compile)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addMenu(menubutton_add_script.menu())
        file_menu.addSeparator()
        file_menu.addMenu(menubutton_run.menu())
        file_menu.addSeparator()
        file_menu.addMenu(menubutton_export.menu())
        file_menu.addSeparator()
        file_menu.addAction("&Quit", self.close)
        self.view_menu = self.menuBar().addMenu("&View")
        self.view_menu.addAction('Toogle Model view', self.toggle_model_view)

        help_menu = self.menuBar().addMenu("&Tutorials")
        for name, tutorial in TutorialViewer.tutorials.items():
            help_menu.addAction(name, lambda name=name, tutorial=tutorial: self.run_tutorial(name, *tutorial))


        help_menu = self.menuBar().addMenu("&About")
        help_menu.addAction("About Qt", qApp.aboutQt)


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
        action = dock.toggleViewAction()
        self.view_menu.addAction(action)
        dock.remove_itself_from_list = lambda a=action, menu=self.view_menu: menu.removeAction(action)
        dock.call_widget_deletion = lambda w=widget: (w._stop() if hasattr(w, '_stop') else None)
        return dock

    def add_default_script(self):
        self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/default.lp"))
    def add_blank_script(self):
        self.add_script_from_file(pkg_resources.resource_filename(__name__, "embedded_scripts/blank.lp"))

    def update_scripts_from_editors(self):
        """ call ScriptEditor.update() on each editor """
        # TODO: make sure that auto_run is not called during that function
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
            dock.remove_itself_from_list()
            dock.call_widget_deletion()  # for tutorials: trigger deletion of QThread
            self.removeDockWidget(dock)
            dock.setParent(None)  # will be soon destroyed

    def current_dot_engine(self) -> str:
        "Return the currently selected dot engine"
        action = self.menubutton_dot_engine_group.checkedAction()
        return action.text() if action else 'dot'


    def run(self):
        """Run biseau and display the dot file"""
        # freeze gui
        self.script_list_widget.setDisabled(True)
        # Update script from editors
        self.update_scripts_from_editors()
        # Create the worker thread
        self.__thread = QThread(self)
        self.__thread.finished.connect(self.__thread.deleteLater)
        self.__thread.start()  # start the thread now, populate with things later
        # Build the main worker, and add it to the thread
        scripts = self.script_list_widget.get_scripts()
        worker = self.__worker = ComputationWorker(scripts=scripts, logger=self.log_widget, script_list_widget=self.script_list_widget)
        worker.moveToThread(self.__thread)
        worker.ASPGenerated.connect(self.set_asp_and_stop)
        worker.run()

    def stop(self):
        """Kill the working thread and worker"""
        self.script_list_widget.setDisabled(False)
        if self.__worker:
            self.__worker.request_stop()
            self.__thread.quit()
            self.__thread.wait()
            self.__thread = None
            self.__worker.deleteLater()
            self.__worker = None

    def auto_run(self):
        if self.auto_run_action.isChecked():
            self.run()


    def clean_cache(self):
        ... # TODO : self.scripting_widget.clear_cache()

    def set_auto_compile(self, active: bool):
        ... # TODO: change button style


    def export_scripts(self):
        "Export current scripts in a single executable file"
        scripts = self.script_list_widget.get_scripts()
        dialog = ScriptExporterDialog(self, scripts)
        dialog.exec_()

    def export_images(self):
        "invoke exporter dialog"
        dialog = OutputExporterDialog(self)
        dialog.exec_()

    def export_outputs(self, template_outfile='out-{tab}', tabs=None, png=False, svg=False, dot=False, asp=False):
        for idx, source in enumerate(self.image_viewer.images_sources(), start=1):
            # ignore tabs that are not wanted
            if tabs is not None and (idx != tabs if isinstance(tabs, int) else idx not in tabs): continue
            # export images and dot if asked to
            if png:
                print('writing', template_outfile.format(tab=idx, ext='png') + '.png')
                source.render(template_outfile.format(tab=idx, ext='png'), format='png', cleanup=True)
            if svg:
                print('writing', template_outfile.format(tab=idx, ext='svg') + '.svg')
                source.render(template_outfile.format(tab=idx, ext='svg'), format='svg', cleanup=True)
            if dot:
                source.save(template_outfile.format(tab=idx, ext='dot') + '.dot')
        if asp:
            print('ASP written in', template_outfile.format(tab='asp', ext='lp') + '.lp')
            with open(template_outfile.format(tab='asp', ext='lp') + '.lp', 'w') as fd:
                fd.write(self.final_asp_context)


    def toggle_model_view(self):
        self._enable_cxt_viewer = not self._enable_cxt_viewer
        self._setup_main_tabs()


    def set_asp(self, context:str):
        "Send dot file to the dot viewer for compilation"
        self.asp_viewer.set_asp(context)

    @Slot(str)
    def set_asp_and_stop(self, context:str):
        self.final_asp_context = context
        self.set_asp(context)
        self.stop()

    @staticmethod
    def start_gui(*args, **kwargs):
        app = QApplication(sys.argv)
        w = MainWindow(*args, **kwargs)
        w.showMaximized()
        return app.exec_()

    def run_tutorial(self, name:str, language:str, sequence:iter, step=0):
        "Remove all scripts, starts the Tutorial view"
        self.tab_widget.setCurrentWidget(self.asp_viewer)  # show the asp code
        self.script_list_widget.remove_all_scripts()
        tuto_interface = TutorialViewer(self, language=language, sequence=sequence, step=step, name_template=name + ' {step}')
        self.script_list_widget.add_script(tuto_interface)
        dock = self._add_as_dock(tuto_interface, name)
        tuto_interface.name_changed.connect(dock.setWindowTitle)

        self._dock_of_script[tuto_interface].append(dock)  # enables to delete it when removing the script
        self.auto_run()


