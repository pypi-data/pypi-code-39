import astroid
import os
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
# from setup_linter import get_path


class AddReferenceChecker(BaseChecker):
    __implements__ = IAstroidChecker
    assembly_list =[]
    setup = False
    name = 'AddReference-notvalid'
    priority = -1
    msgs = {
        'E8101': (
            'AddReference is not valid.',
            'AddReference-cant-be-found',
            'AddReference string should be a valid module.'
        ),
    }
    options = (
        (
            "boxwise-paths",
            {
                "default": ("C:\Program Files (x86)\TranCon\BOXwisePro\Server"),
                "type": "csv",
                "metavar": "<names>",
                "help": "Default location of boxwise installation server dir so ending in ..\TranCon\BOXwisePro\Server",
            },
        ),
        (
            "module-name-contains",
            {
                "default": ("TranCon","Wms"),
                "type": "csv",
                "metavar": "<names>",
                "help": "Add which modules need to be checked",
            }
        )

    )

    def __init__(self, linter=None):
        super(AddReferenceChecker, self).__init__(linter)


    def setup_after_pylinrc_read(self):
        self.setup = True
        for path in self.config.boxwise_paths:
            for file_path in os.listdir(path):
                if file_path.endswith('.dll'):
                    self.assembly_list.append(file_path[:-4])


    def visit_call(self, node):
        if not self.setup:
            self.setup_after_pylinrc_read() 
        try:
            if node.func.expr.name == 'clr' and node.func.attrname == 'AddReference':
                path = node.args[0].value
                if path not in self.assembly_list and any([path.startswith(x) for x in self.config.module_name_contains]):
                    self.add_message('AddReference-cant-be-found', node=node)
        except: #catch if the function doesn't reference an external source.
            return

