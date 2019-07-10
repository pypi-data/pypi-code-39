from IPython.display import display
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring
from IPython.core.magic import line_magic, cell_magic, Magics, magics_class

from .filemanager import FileManager
from .editorwidget import EditorWidget

@magics_class
class SourceMagics(Magics):
    def __init__(self, shell):
        super(SourceMagics, self).__init__(shell)
        self.file_manager = FileManager()

    @line_magic
    @magic_arguments()
    @argument('path', type=str, help='Source path')
    def loadsource(self, line=''):
        """
        Load file for editing (replaces cell content)
        """
        args = parse_argstring(self.loadsource, line)
        self.shell.set_next_input("%%source " + line + "\n" + self.file_manager.read(args.path), replace=True)

    @cell_magic
    @magic_arguments()
    @argument('path', type=str, help='Source path')
    @argument("-p", "--pooling-rate",
              type=int,
              default=500,
              help="pooling rate for external file modifications in milliseconds. Set to 0 to disable it (default: 500)"
    )
    @argument("--no-eval",
              help="do not evaluate contents",
              action='store_true'
    )
    @argument("--debug",
              help="Display debugging info",
              action="store_true"
    )
    def source(self, line='', cell=""):
        """
        Run and write the contents of the cell to a file.

        If file exists and cell and file are out of sync, prompts what to do (see args to override).

        Periodically pools for external file modifications (see args to override).
        """
        args = parse_argstring(self.source, line)
        editor_widget = EditorWidget(file_manager = self.file_manager, \
                                     shell = self.shell, \
                                     line = line, \
                                     cell = cell, \
                                     path = args.path, \
                                     no_eval = args.no_eval, \
                                     conflict_resolution_strategy = args.conflict_resolution_strategy, \
                                     pooling_rate = args.pooling_rate, \
                                     debug = args.debug)
        display(editor_widget)
        editor_widget.process_cell_execution()
        editor_widget.check_external_modification()

    arg_group = source.parser.add_mutually_exclusive_group()
    arg_group.add_argument('--prompt', \
                           help="prompt what to do if cell and file are out of sync (default)", \
                           action='store_const', dest='conflict_resolution_strategy', const='Prompt', default='Prompt')
    arg_group.add_argument('--keep-both', \
                           help="if cell and file are out of sync keep both untouched, proceed with execution", \
                           action='store_const', dest='conflict_resolution_strategy', const='Keep Cell Contents and Continue Execution')
    arg_group.add_argument('--overwrite-existing', \
                           help="overwrite existing file without confirmation", \
                           action='store_const', dest='conflict_resolution_strategy', const='Overwrite File and Continue Execution')
    arg_group.add_argument('--abort', \
                           help="abort notebook execution if cell and file are out of sync", \
                           action='store_const', dest='conflict_resolution_strategy', const='Abort')

    source.__doc__ = source.parser.format_help()
