import os
import json


def writeconfiguration(absolute_path, variables, overwrite=False):
    """
    Write a config file with provided, optionally separated, variables
    :param absolute_path: String; path of the output file
    :param variables: Dict; variables to write to the file
    :param overwrite: Boolean; Should any present file be overwritten?
    :return: None
    """
    if not overwrite:
        if os.path.isfile(absolute_path):
            raise FileExistsError("There is already a file at " + absolute_path)
    with open(absolute_path, 'w+') as cfg:
        for var in variables:
            if type(variables[var]) == dict:
                variables[var] = json.dumps(variables[var])
            if var[0] == "#":
                cfg.write('#' + variables[var] + '\n')
                continue
            if variables[var][0] == ";":  # Is this an additive or definite variable?
                values = variables[var].split(variables[var][1])[1:]
                for i in values:
                    cfg.write(var + "; " + i + '\n')
            else:
                cfg.write(var + ": " + variables[var].strip() + '\n')


def readfile(absolute_path):
    """
    Read a config file at the path provided
    :param absolute_path: String; path of the config file
    :return: Dict; Variables read from the file
    """
    output = {}

    if not os.path.isfile(absolute_path):
        raise FileNotFoundError("There is no file at " + absolute_path)
    with open(absolute_path, 'r') as cfg:
        for line in cfg:
            line = [char for char in line]
            semicolon = None
            for char in line:
                if char == ";":
                    semicolon = True
                    break
                if char == ":":
                    semicolon = False
                    break
                if char == "#":
                    break
            line = ''.join(line)
            if semicolon is True:
                line = line.split('; ')
                if line[0] in output:
                    output[line[0]] += ',' + '; '.join(line[1:]).strip()
                else:
                    output.update({line[0]: '; '.join(line[1:]).strip()})
            elif semicolon is False:
                line = line.split(': ')
                output.update({line[0]: ': '.join(line[1:]).strip()})
            elif semicolon is None:
                continue
    return output
