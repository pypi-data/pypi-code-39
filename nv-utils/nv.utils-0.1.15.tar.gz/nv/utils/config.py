import json
import pickle

from importlib.util import find_spec
from pathlib import Path

from nv.utils.formatters import format_structure


__all__ = ['load', 'dump', 'parse_instructions', 'merge_instructions']


class ConfigParserException(Exception):
    pass


class Parser:
    def __init__(self, parse, serialize, is_binary=False):
        self.parse = parse
        self.serialize = serialize
        self.is_binary = is_binary


PARSERS = {
    'json': Parser(json.loads, json.dump),
    'pickle': Parser(pickle.loads, pickle.dump, True),
    'pck': Parser(pickle.loads, pickle.dump, True),
}

if find_spec('yaml'):
    import yaml
    PARSERS.update({
        'yml': Parser(yaml.safe_load, yaml.safe_dump),
        'yaml': Parser(yaml.safe_load, yaml.safe_dump),
    })

if find_spec('hcl'):
    import hcl
    PARSERS.update({
        'hcl': Parser(hcl.loads, json.dump),
    })


def choose_parser(fp):
    fp = Path(fp)
    ext = fp.suffix[1:] if fp.suffix.startswith('.') else fp.suffix
    parser = PARSERS.get(ext, None)

    if not parser:
        raise RuntimeError('Missing parser for {fp_suffix}'.format(fp_suffix=fp.suffix))

    return parser


def load(fp, defaults=None, missing=False, clean_up=False):
    """
    This is a helper to load and parse config files through a typical Python string formatter (i.e. {key} becomes
    value). Variable substitution is ran after content is parsed. This avoids dealing with json/hcl structural brackets.
    However, brackets inside strings must be escaped or duplicated ('{{') to stay if further parsing is necessary.
    :param fp: file
    :param defaults: key-value dictionary for variable substitution
    :param missing: if True, variable substitution will leave missing variables intact. Otherwise, a
    ConfigParserException will be raised (default behaviour).
    :param clean_up: If True, empty substructures such as {}, [], '' and anything else that evaluates to 'False' will be
    removed.
    :return: parsed structure (i.e. dict, array or string, or any structure made out of these primitives).
    """
    fp = Path(fp)
    parser = choose_parser(fp)

    # Load file content
    try:
        with fp.open(mode='rb' if parser.is_binary else 'r') as f:
            content = f.read()
    except Exception as e:
        raise ConfigParserException(
            'Unable to read from {fp} due to: {e}'.format(
                fp=fp,
                e=e
            )
        ) from e

    # Parse content
    try:
        content = parser.parse(content)
    except Exception as e:
        raise ConfigParserException(
            'Unable to parse {fp} due to: {e}'.format(
                fp=fp,
                e=e
            )
        ) from e

    # Runs variable substitution
    if defaults:
        try:
            content = format_structure(content, defaults, missing=missing, clean_up=clean_up)
        except Exception as e:
            raise ConfigParserException(
                'Exception occurred while parsing variables in {fp}: {e}'.format(
                    fp=fp,
                    e=e
                )
            ) from e

    return content


def dump(content, fp):
    parser = choose_parser(fp)
    with fp.open(mode='wb' if parser.is_binary else 'w') as f:
        parser.serialize(content, f)


def _parse_instruction(instruction, variables):
    if callable(instruction):
        # If callable, calls it - whatever returns, it is the result
        return instruction()

    if isinstance(instruction, (tuple, list)):
        instruction, default = instruction
        return variables.get(instruction, default)

    if isinstance(instruction, str):
        return variables.get(instruction, None)

    raise ValueError('Unrecognized instruction: {instruction}'.format(instruction=instruction))


def parse_instructions(instructions, variables):
    # Parse instructions
    results = dict()
    for entry, value in instructions.items():
        result = _parse_instruction(value, variables)

        if result:
            results[entry] = result
    return results


def merge_instructions(fp, instructions, defaults=None, update_file=False):
    content = load(fp, defaults=defaults)
    results = parse_instructions(instructions, defaults)
    content = {**content, **results}
    if update_file:
        dump(content, fp)
    return content


def load_from_path(path, base_file_name, optional=True, **kwargs):
    config_file = None

    for extension in PARSERS.keys():
        config_file = path / ("{base_file_name}.{extension}").format(base_file_name=base_file_name, extension=extension)
        if config_file.exists():
            break
    else:
        config_file = None

    if config_file is None:
        if not optional:
            msg = "ERROR: Unable to load any config file at: {path}/{base_file_name}.{{{extensions}}}".format(
                path=path,
                base_file_name=base_file_name,
                extensions=','.join(PARSERS.keys())
            )
            raise ConfigParserException(msg)
        else:
            return {}

    return load(config_file, **kwargs)
