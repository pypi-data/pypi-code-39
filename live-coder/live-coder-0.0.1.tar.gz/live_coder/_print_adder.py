import ast
import astor
import copy
import json

from ._get_variables import variables_in_commands, functions_in_commands
from ._string_tools import get_tab_length, get_line_tab, remove_tab, add_tab

from ._constants import (
    LOOP_TYPE,
    IF_TYPE,
    BODY_KEY,
    LOOP_KEY,
    IF_KEY_TEMPLATE,
    BREAK_KEY,
    LOOP_BREAK_TEMPLATE,
    SPLIT_KEY,
    SUBSPLIT_KEY,
    LABEL_TEMPLATE,
    VARIABLE_KEY,
    FUNCTION_KEY
)
QUOTED_PRINT_TEMPLATE = "print('{0}')"
SINGLE_TAB = ' '*4

class PrintAdder:

    def __init__(self, file_path, function_def_root, top_level_commands, class_name=None):
        '''
            Adds print statements to a function.
            @params:
                file_path: path of the file holding the function
                function_def_root: ast.FunctionDef node of the functions AST
                class_name: name of the class holding the function, None => no class

            @returns:
                ast.FunctionDef with added print statements in it's body
        '''
        self.file_path = file_path
        self.function_def_root = function_def_root

        self.referenced_variabels = set()
        self.loop_count = 0

        self.top_level_commands = top_level_commands
        self.defined_functions = self._get_defined_functions()

        self.class_name = class_name

    def _get_defined_functions(self):
        '''
            Get set of defined function names and imported names.
        '''
        all_functions = set()
        for command in self.top_level_commands:
            if type(command) is ast.FunctionDef:
                all_functions.add(command.name)
            elif type(command) is ast.Import or type(command) is ast.ImportFrom:
                imports = [] if type(command) is ast.Import else [command.module]
                for alias in command.names:
                    imports.append(alias.name)
                all_functions.update(set(imports))
        return all_functions

    @staticmethod
    def _new_print_statement(obj, code=''):
        json_str = json.dumps(obj)
        formatted_json = json_str.replace('"', '\\"')
        if type(code) is list:
            joiner = ', "{0}", '.format(SPLIT_KEY)
            code = joiner.join([str(snippet) for snippet in code])
        return ast.parse(
            'print("{0}", "{1}", {2})'.format(formatted_json, SPLIT_KEY, code)
        ).body[0]

    def _new_var_print(self, line_number, var, **attributes):
        attributes['type'] = 'variable'
        if 'label' not in attributes:
            attributes['label'] = var
        if 'value' not in attributes:
            value = var
        else:
            value = attributes['value']
            del attributes['value']
        if 'is_self' not in attributes and var == 'self':
            return None
        attributes['line_number'] = line_number
        return self._new_print_statement(attributes, code=value)

    @staticmethod
    def _new_break_print(break_key):
        return ast.parse(
            QUOTED_PRINT_TEMPLATE.format(break_key)
        ).body[0]

    def _new_function_print(self, line_number, function_name, arguments_code_snippets):
        attributes = {
            'type': 'function',
            'name': function_name,
            'line_number': line_number
        }
        return self._new_print_statement(attributes, code=arguments_code_snippets)

    def _print_functions(self, line_number, functions):
        print_statements = []
        for func in functions:
            print_statements.append(
                self._new_function_print(line_number, func['name'], func['arguments'])
            )
        return print_statements

    def _print_vars(self, line_number, variables, **shared_attributes):
        self.referenced_variabels.update(variables)
        print_statements = []
        for var in variables:
            a_print = self._new_var_print(line_number, var, **shared_attributes)
            if a_print:
                print_statements.append(a_print)
        return print_statements

    def _get_args(self):
        args = []
        for arg in self.function_def_root.args.args:
            args.append(arg.arg)
        return args

    def _print_args(self):
        commands = []
        args = self._get_args()
        if 'self' in args:
            commands.append(
                self._new_var_print(None, None, is_arg=True, is_self=True)
            )
            args.remove('self')
        commands += self._print_vars(None, args, is_arg=True)
        return commands

    def _print_def_call(self):
        name = self.function_def_root.name
        if self.class_name:
            name = self.class_name + '.' + name
        return self._new_print_statement(
            {
                'type': 'function_call', 'name': name,
                'file_path': self.file_path, 'line_number': self.function_def_root.lineno
            }
        )

    def _print_def(self):
        commands = []
        commands.append(self._print_def_call())
        commands += self._print_args()
        commands.append(self._new_break_print(BREAK_KEY))
        return commands

    @staticmethod
    def _command_to_source(command):
        source_lines = astor.to_source(command)[:-1].split('\n')
        return add_tab(
            4 + command.col_offset,
            source_lines
        )

    def _print_return(self, a_command):
        returning_value_ast = a_command.value
        returning_value_code = astor.to_source(returning_value_ast)[:-1]
        return_print = self._new_var_print(
            a_command.lineno,
            returning_value_code,
            label='return'
        )
        commands = []
        if return_print:
            commands.append(return_print)
        commands.append(a_command)
        return commands

    @staticmethod
    def _is_a_print_command(command):
        return (
            type(command) is ast.Expr
            and type(command.value) is ast.Call
            and type(command.value.func) is ast.Name
            and command.value.func.id == 'print'
        )

    def _print_a_print(self, command):
        arg_strings = []
        for arg in command.value.args:
            arg_strings.append(
                astor.to_source(arg)[:-1]
            )
        attributes = {'type': 'print', 'line_number': command.lineno}
        return [self._new_print_statement(attributes, code=arg_strings)]

    def _print_command(self, a_command):
        commands = []
        functions = functions_in_commands(self.defined_functions, [a_command])
        commands += self._print_functions(a_command.lineno, functions)
        commands.append(a_command)
        variables = variables_in_commands(self.defined_functions, [a_command])
        commands += self._print_vars(a_command.lineno, variables)
        return commands


    def _new_loop_id(self):
        self.loop_count += 1
        return self.loop_count

    def _get_loop_attributes(self, command):
        loop_id = self._new_loop_id()
        return {'type': 'loop_start', 'line_number': command.lineno, 'id': loop_id}

    def _print_loop_break(self, loop_id):
        break_key = LOOP_BREAK_TEMPLATE.format(loop_id)
        return self._new_break_print(break_key)

    def _print_loop_end(self, attributes):
        attributes['type'] = 'loop_end'
        return self._new_print_statement(attributes)

    def _print_what_for_is_iterating(self, target):
        if type(target) is ast.Name:
            variable_name = target.id
            a_print = self._new_var_print(target.lineno, variable_name, must_print=True)
            if a_print:
                return [a_print]
            return []
        if type(target) is ast.Tuple:
            print_commands = []
            for name_command in target.elts:
                name = name_command.id
                a_print = self._new_var_print(name_command.lineno, name, must_print=True)
                if a_print:
                    print_commands.append(a_print)
            return print_commands
        raise RuntimeError('Unknown type in for loop.')


    def _print_loop_body(self, loop_command, loop_id):
        new_body = []
        if type(loop_command) is ast.For:
            new_body += self._print_what_for_is_iterating(loop_command.target)
        new_body += self._add_prints_to_commands(loop_command.body)
        new_body.append(self._print_loop_break(loop_id))
        return new_body


    def _print_loop(self, loop_command):
        attributes = self._get_loop_attributes(loop_command)
        commands = [self._new_print_statement(attributes)]
        loop_command.body = self._print_loop_body(loop_command, attributes['id'])
        commands.append(loop_command)
        commands.append(self._print_loop_end(attributes))
        return commands


    def _find_conditions(self, if_command):
        conditions = [
            {
                'condition': astor.to_source(if_command.test)[:-1],
                'line_number': if_command.lineno
            }
        ]
        if len(if_command.orelse) == 0:
            return conditions
        or_else = if_command.orelse[0]
        if type(or_else) is ast.If:
            conditions += self._find_conditions(or_else)
        else:
            conditions.append({'condition': 'else'})
        return conditions


    def _print_if_checks(self, starting_lineno, if_command):
        attributes = {
            'type': 'if',
            'id': starting_lineno,
            'line_number': starting_lineno,
            'conditions': []
        }
        code_snippets = []
        conditions = self._find_conditions(if_command)
        passed_if = False
        for condition_info in conditions:
            if condition_info['condition'] == 'else':
                attributes['conditions'].append({'label': 'else:'})
                code_snippets.append(True)
            else:
                if passed_if is False:
                    if_type = 'if'
                    passed_if = True
                else:
                    if_type = 'elif'
                label = '{0} {1}:'.format(if_type, condition_info['condition'])
                attributes['conditions'].append({'label': label, 'line_number': condition_info['line_number']})
                code_snippets.append(condition_info['condition'])
        return self._new_print_statement(attributes, code=code_snippets)

    def _print_if(self, if_command):
        '''
        AST.If
            .body = list of commands
            .test = if statement
            .orelse = (in a len 1 list) elif statement OR else list of commands
        '''
        if_checks = self._print_if_checks(if_command.lineno, if_command)
        root_if_command = if_command
        while if_command:
            if_command.body = self._add_prints_to_commands(if_command.body)
            or_else = if_command.orelse
            if len(or_else) == 0:
                break
            elif type(or_else[0]) is ast.If:
                if_command = or_else[0]
            elif len(or_else) > 0:
                if_command.orelse = self._add_prints_to_commands(or_else)
                break
        return [if_checks, root_if_command]


    def _prints_with_command(self, command):
        c_type = type(command)
        if c_type in [ast.For, ast.While, ast.If]:
            if c_type in [ast.For, ast.While]:
                return self._print_loop(command)
            if c_type is ast.If:
                return self._print_if(command)
        if self._is_a_print_command(command):
            return self._print_a_print(command)
        return self._print_command(command)


    def _prints_with_breaks_with_command(self, command):
        break_command = self._new_break_print(BREAK_KEY)
        if type(command) is ast.Return:
            return [break_command] + self._print_return(command)
        commands_with_prints = self._prints_with_command(command)
        return [break_command] + commands_with_prints + [break_command]


    @staticmethod
    def _next_command_lineno(commands, i, command_after_last_lineno):
        if i+1 >= len(commands):
            return command_after_last_lineno
        return commands[i + 1].lineno

    def _add_prints_to_commands(self, commands):
        commands_with_prints = []
        for command in commands:
            commands_with_prints += self._prints_with_breaks_with_command(command)
        return commands_with_prints

    def run(self):
        new_body = []
        new_body += self._print_def()
        new_body += self._add_prints_to_commands(
            self.function_def_root.body
        )
        if type(self.function_def_root.body[-1]) is not ast.Return:
            new_body.append(self._new_print_statement({'type': 'function_end'}))
        self.function_def_root.body = new_body
        return self.function_def_root

