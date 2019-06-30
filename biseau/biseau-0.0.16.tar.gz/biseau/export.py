"""Routines for the export of scripts to various form

"""

import biseau as bs
import datetime
import itertools
from functools import wraps
from . import Script, __version__
try:
    import black
except ImportError:
    black = None

def repr_argument_type(ctype) -> str:
    """Return the represenation of a biseau argument type, ready to be use
    to generate the annotations of run_on function."""
    if ctype in {int, float, str, bool}:
        return ctype.__name__
    elif ctype is open or ctype == (open, 'r'):
        return 'open'
    elif ctype == (open, 'w'):
        return "(open, 'w')"
    elif isinstance(ctype, range):
        return "range({ctype.start}, {ctype.stop}, {ctype.step})"
    elif isinstance(ctype, (int, float, str, bool, list, tuple, set, frozenset, dict)):
        return repr(ctype)
    else:
        raise NotImplementedError(f"Type '{type}' cannot be represented as an argument type")

def get_pipeline_options(scripts:[Script]) -> dict:
    """Return the mapping option->False to be used by standalone_export_pipeline.

    One may want to set some options to True, to get them in pipeline standalone export.

    """
    return {n: False for _, __, n in option_names_from_options(scripts)}


def _standalone_export_pipeline(scripts:[Script], options:dict={}, default_context:str='',
                                metarg_withgui:bool=True, metarg_outfile:str='out.png', metarg_dotfile:str='out.dot',
                                metarg_dot_prog:str='dot', verbosity:int=0, name:str='Standalone script') -> [str]:
    """Yield Python code strings, implementing a standalone program reproducing given pipeline.

    options -- {option name: bool} indicating whether or not the option
               must be exposed as program option.
    default_context -- the default initial context.
    verbosity -- verbosity of the standalone program itself.

    """
    option_names = {(idx, name): final_name for idx, name, final_name in option_names_from_options(scripts)}
    # print('OPTIONS NAMES:', option_names)
    # print('RECOGNIZED OPTIONS:', options)
    options_used = tuple(
        ((idx, name), final_name) for (idx, name), final_name in option_names.items()
        if options.get(final_name)
    )
    def options_as_dict(opts):
        return {name: vals for name, *vals in opts}

    # print('OPTIONS USED:', options_used)
    yield f'"""{name}'
    yield f'Generated by biseau {__version__}, {datetime.datetime.now()}.'
    yield '\n"""\n'
    yield 'import os'
    yield 'import argparse'
    if metarg_withgui:  yield 'from clitogui import clitogui'
    yield 'import clyngor'
    yield 'import biseau'
    yield ''
    if options_used:
        if metarg_withgui:  yield '@clitogui.clitogui'
        yield 'def cli():'
        yield '    def existing_file(filepath:str) -> str:'
        yield '        """Argparse type, raising an error if given file does not exists"""'
        yield '        if not os.path.exists(filepath):'
        yield '            raise argparse.ArgumentTypeError("file {} doesn\'t exists".format(filepath))'
        yield '        return filepath'
        yield '    def writable_file(filepath:str) -> str:'
        yield '        """Argparse type, raising an error if given file is not writable.'
        yield '        Will delete the file !"""'
        yield '        try:'
        yield '            with open(filepath, "w") as fd:'
        yield '                pass'
        yield '            os.remove(filepath)'
        yield '            return filepath'
        yield '        except (PermissionError, IOError):'
        yield '            raise argparse.ArgumentTypeError("file {} is not writable.".format(filepath))'
        yield '    parser = argparse.ArgumentParser(description=__doc__)'
        yield '    def elem_in_list(elements:iter):'
        yield '        def valid_element(element:str) -> str:'
        yield '            """Argparse type, raising an error if given value is not expected"""'
        yield '            if element not in elements:'
        yield '                raise argparse.ArgumentTypeError(f"Value {element} is unexpected. Valid inputs: " + ", ".join(map(str, elements)))'
        yield '            return element'
        yield '        return valid_element'
        for (idx, name), final_name in options_used:
            option = options_as_dict(scripts[idx].options)[final_name]
            func, args = argparse_addarg_args_from_option(final_name, option, explicit_value=scripts[idx].options_values.get(name))
            yield f'    parser.{func}({", ".join(args)})'
            # print('MAKE ARG:', f'    parser.{func}({", ".join(args)})')
        yield '    return parser'
        yield ''
    else:
        if metarg_withgui:  yield '@clitogui.clitogui'
        yield 'def cli():'
        yield '    parser = argparse.ArgumentParser(description=__doc__)'
        yield '    return parser'
    # add a run_on function for each script
    runons = []
    for script in scripts:
        bs.utils.name_to_identifier(script.name)
        runon_name = f"run_on_{bs.utils.name_to_identifier(script.name)}"
        runons.append((runon_name, script))
    for runon_name, script in runons:
        params = ', '.join(f"{name}:{valtype.__name__ if type(valtype) in {type(open), type(bool)} else str(valtype)}={repr(default)}" for name, valtype, default, _ in script.options)
        yield f'def {runon_name}(context, {params}):'
        if script.language == 'python':
            for line in script.source_code.splitlines(False):
                yield '    ' + line
            runon_args = ', '.join(f"{name}={name}" for name, *_ in script.options)
            new_context = f"''.join(run_on(context, {runon_args}))"
        elif script.language == 'asp':
            new_context = '"""' + script.source_code + '"""'
        elif script.language == 'asp file':
            yield f'    def run_on(context):'
            yield f'        with open("{script.source_code}") as fd:'
            yield r'             return context + "\n" + fd.read().strip()'
            new_context = f"run_on(context)"
        else:
            raise ValueError(f"unhandled export of language '{script.language}'")
        if not script.erase_context:
            new_context = r'context + ("\n" if context else "") + ' + new_context
        yield f'    return {new_context}'

    # informations about the script, for biseau
    yield f'NAME = {name}'
    yield f'TAGS = {repr(set.union(*(script.tags for script in scripts)))}'
    outputs = set.union(*(set(script.outputs()) for script in scripts))
    inputs = set.union(*(set(script.inputs()) for script in scripts))
    yield f'OUTPUTS = {repr(outputs - inputs)}'  # expose what is not used
    yield f'INPUTS = {repr(inputs - outputs)}'

    # write the main run_on function, expecting all parameters
    main_args = []
    for (idx, name), final_name in options_used:
        ctype, default, help = options_as_dict(scripts[idx].options)[name]
        main_args.append(f"{final_name}:{repr_argument_type(ctype)}={repr(default)}")
    main_args = ', '.join(main_args)
    yield f'def run_on(context:str, *, {main_args}):'

    # call each *_run_on inside the run_on, taking care to provide its arguments
    for runon, script in runons:
        target_idx = scripts.index(script)
        options = ((name, final_name) for (idx, name), final_name in options_used if idx == target_idx)
        args = ', '.join(f"{name}={final_name}" for name, final_name in options)
        yield f'    context = {runon}(context, {args})'

    yield f'    biseau.compile_to_single_image(context, outfile={repr(metarg_outfile)}, dotfile={repr(metarg_dotfile)}, dot_prog={repr(metarg_dot_prog)}, verbosity={repr(verbosity)})'
    yield '    return context'
    yield 'if __name__ == "__main__":'
    yield '    args = cli().parse_args()'
    yield '    context = ' + repr(default_context)
    # calling the main run_on
    all_args = ', '.join(f'{final_name}=args.{final_name}' for (idx, name), final_name in options_used)
    yield f'    run_on(context, {all_args})'


def option_names_from_options(scripts:[Script]) -> [(int, str, str)]:
    """Yield (script idx, option name, unambiguous option name)
    so that unambiguous option name is deterministic and unique
    accross all options of given scripts.

    """
    scripts = tuple(scripts)
    used_names = set()  # set of all available options
    conflicting_names = set()  # names that will need the script name
    script_names = tuple(script.name for script in scripts)
    script_indexes = tuple(idx for idx, script in enumerate(scripts))
    script_name_doublons = {n: itertools.count(1) for n in script_names if script_names.count(n) > 1}
    # define names of scripts (append their index when multiple scripts of same name)
    script_names = tuple(
        (script.name + ' ' + str(next(script_name_doublons[script.name])))
        if script.name in script_name_doublons else script.name
        for script in scripts
    )
    assert len(script_names) == len(scripts)
    # detect the name conflicts among scripts options
    for script in scripts:
        for name, type, default, description in script.options:
            if name in used_names:
                conflicting_names.add(name)
            used_names.add(name)
    # for each script, ensure the use of proper option name
    for idx, script_name, script in zip(script_indexes, script_names, scripts):
        for name, type, default, description in script.options:
            final_name = name
            if name in conflicting_names:
                final_name = f'{script_name}_{name}'
            yield idx, name, final_name


def argparse_addarg_args_from_option(name:str, option, *, explicit_value=None) -> [str]:
    # print('creating argparse arguments:', name, option)
    argtype, default, description = option
    if explicit_value is not None:  default = explicit_value  # override default
    if argtype is open:
        ctype = 'existing_file'
    elif isinstance(argtype, tuple) and len(argtype) == 2 and argtype[0] is open:
        mode = argtype[1]
        if mode == 'r':
            ctype = 'existing_file'
        elif mode == 'w':
            ctype = 'writable_file'
    elif isinstance(argtype, (list, tuple)):
        ctype = 'elem_in_list((' + ', '.join(map(repr, argtype)) + '))'
    elif argtype is str:
        ctype = 'str'
    elif argtype is bool:
        ctype = 'bool'
        default = 'false' if default else 'true'
        return 'add_argument', (f"'--{name}'", f'action="store_{default}"', f'help="{description}"')
    elif argtype is int:
        ctype = 'int'
    elif argtype is float:
        ctype = 'float'
    else:
        raise NotImplementedError(f"Option of type {argtype} cannot be transcripted as widget")
    return 'add_argument', (f"'{name}'", f'type={ctype}', f'default={repr(default)}', f'help="{description}"')


@wraps(_standalone_export_pipeline)
def standalone_export_pipeline(*args, **kwargs) -> [str]:
    """Return a string of Python code, implementing a standalone program reproducing given pipeline.
    Also takes care of formatting it with black, if available.

    options -- {option name: bool} indicating whether or not the option
               must be exposed as program option.
    default_context -- the default initial context.
    verbosity -- verbosity of the standalone program itself.

    """
    python_code = standalone_export_pipeline_without_formatting(*args, **kwargs)
    if black:
        return black.format_str(python_code, mode=black.FileMode())
    return python_code


@wraps(_standalone_export_pipeline)
def standalone_export_pipeline_without_formatting(*args, **kwargs) -> [str]:
    """Return a string of Python code, implementing a standalone program reproducing given pipeline.

    options -- {option name: bool} indicating whether or not the option
               must be exposed as program option.
    default_context -- the default initial context.
    verbosity -- verbosity of the standalone program itself.

    """
    gen = _standalone_export_pipeline(*args, **kwargs)
    python_code = '\n'.join(gen)
    return python_code

standalone_export_pipeline.without_formatting = standalone_export_pipeline_without_formatting
