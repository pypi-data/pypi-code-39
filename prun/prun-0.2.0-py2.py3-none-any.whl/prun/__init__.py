import glob
import os
import sys
import subprocess
import shutil

_platform_dict = {'win32': {'msg_not_found': "'%s' is not recognized as an internal or external command,\n"
                                             "operable program or batch file.",
                            'exec_folder': 'Scripts',
                            'exec_name': 'python.exe',
                            '-show': 'where'},
                  'darwin': {'msg_not_found': '%s: command not found',
                             'exec_folder': 'bin',
                             'exec_name': 'python',
                             '-show': 'which'}
                  }

_venv_names = ['.venv', 'venv']


def main():
    # system dependent variables
    sys_vars = _platform_dict[sys.platform]
    exec_folder = sys_vars['exec_folder']
    exec_name = sys_vars['exec_name']
    msg_not_found = sys_vars['msg_not_found']

    # get the current working directory
    current_dir = os.getcwd()

    # get the command line arguments
    cli_args = sys.argv[1:]

    # search the python executable folder in the current working directory
    python_exec = search_python_in_folder_structure(current_dir, exec_folder, exec_name)
    if python_exec is None:
        raise ValueError('No virtual environment was found')
    python_folder = os.path.dirname(python_exec)

    # Add the python executable folder to the path environment variable
    env = os.environ.copy()
    env['PATH'] = os.pathsep.join(filter(None, [python_folder, os.environ.get('PATH', '')]))

    # process the command line arguments for special tasks
    cli_args = process_cli_args(cli_args=cli_args, env_path=env['PATH'], platform_vars=sys_vars)
    if cli_args[0] is None:
        print(msg_not_found % cli_args[0])
        sys.exit(1)

    # Run the command
    try:
        p = subprocess.run(cli_args, universal_newlines=True, env=env)
        sys.exit(p.returncode)
    except FileNotFoundError:
        print(msg_not_found % cli_args[0])
        sys.exit(1)


def process_cli_args(cli_args, env_path, platform_vars):
    """
    Process the list of command line arguments.

    Args:
        cli_args (list of str): list of command line arguments
        env_path (str): path for finding executables to construct cli args
        platform_vars (dict): platform dependent variables

    Returns:
        list of str: processed list of command line arguments
    """

    if len(cli_args) == 0:
        # if no cli args, add python
        cli_args = [platform_vars['exec_name']]

    if cli_args[0].endswith('.py'):
        # if first argument is a python file, add python
        cli_args = [platform_vars['exec_name']] + cli_args

    if cli_args[0] == '-show':
        # if first argument is -show, show the path to the found python
        cli_args = [platform_vars['-show'], platform_vars['exec_name']]
    elif cli_args[0] == '-h' or cli_args[0] == '-help':
        print('prun help: \n'
              '  Running a command using the local virtual environment:\n'
              '    prun command arg1 arg2 ...\n'
              '  Running python from the local virtual environment:\n'
              '    prun\n'
              '  Running a python file from the local virtual environment:\n'
              '    prun script.py arg1 arg2\n'
              '  Show the path to the python executable of the virtual environment:\n'
              '    prun -show\n'
              '  Show the prun help\n'
              '    prun -h')
        sys.exit(0)
    else:
        # cli_args[0] is an executable
        cli_args[0] = shutil.which(cli_args[0], path=env_path)

    return cli_args


def search_python_in_folder_structure(folder, exec_folder_name, exec_name, max_search_depth=100):
    """
    Search a folder structure for a virtual environment python executable.

    Args:
        folder (str): the folder to start the search
        exec_folder_name (str): folder name of python executable
        exec_name (str): name of python executable
        max_search_depth (int): maximum upward search depth

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    folder_name = None
    for i in range(max_search_depth):
        if folder_name == '':
            break

        python_exec = find_virtual_environment(folder, exec_folder_name, exec_name)
        if python_exec is not None:
            return python_exec

        folder, folder_name = os.path.split(folder)
    return None


def find_virtual_environment(folder, exec_folder_name, exec_name):
    """
    Search a single folder for a virtual environment python executable.

    Args:
        folder (str): folder to find the virtual environment python executable in
        exec_folder_name (str): folder name of python executable
        exec_name (str): name of python executable

    Returns:
        str or None: path to the python executable or None if it was not found
    """
    glob_paths = [os.path.join(folder, v, exec_folder_name, exec_name) for v in _venv_names]
    python_exec = None
    for glob_path in glob_paths:
        try:
            python_exec = glob.glob(glob_path)[0]
        except IndexError:
            continue
        break

    return python_exec
