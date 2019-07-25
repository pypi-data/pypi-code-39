import ast
import astor

from ._print_adder import PrintAdder
from ._string_tools import add_tab


def _parse_function(file_path, root, top_level_commands, class_name=None):
    # root = _remove_tab(root)
    print_adder = PrintAdder(file_path, root, top_level_commands, class_name=class_name)
    return print_adder.run()


def _remove_tab(root):
    if hasattr(root, 'col_offset'):
        root.col_offset -= 4
    for child in ast.iter_child_nodes(root):
        _remove_tab(child)
    return root


def _parse_class(file_path, root, top_level_commands):
    class_name = root.name
    # root = _remove_tab(root)
    new_body = []
    for command in root.body:
        if type(command) is ast.ClassDef:
            new_body.append(_parse_class(file_path, command, top_level_commands))
        elif type(command) is ast.FunctionDef:
            new_body.append(_parse_function(file_path, command, top_level_commands, class_name=class_name))
        else:
            new_body.append(command)
    root.body = new_body
    return root


def add_execution_prints(file_path, root):
    '''
        Add prints to show the execution of every function in the code.
    '''
    new_body = []
    for command in root.body:
        if type(command) is ast.ClassDef:
            new_body.append(
                _parse_class(file_path, command, root.body)
            )
        elif type(command) is ast.FunctionDef:
            new_body.append(
                _parse_function(file_path, command, root.body)
            )
        else:
            new_body.append(command)
    root.body = new_body
    return astor.to_source(root)[:-1]


