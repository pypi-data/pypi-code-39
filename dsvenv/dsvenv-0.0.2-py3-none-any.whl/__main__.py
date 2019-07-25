from argparse import ArgumentParser
import os
import subprocess
import sys
import tempfile


def get_venv_executable(venv_dir, executable, required=True):
    """
    Return the full path to an executable inside a given virtual environment.

    Args:
        venv_dir (str): Path to the directory containing the virtual environment.
        executable (str): Name of the executable.
        required (bool): Whether to consider it a fatal error if the executable is not found.

    Returns:
        str or None: Full path to an executable inside the virtual environment. In case it cannot be found,
                     either an exception is raised or None is returned, depending on whether the executable is
                     required or not.

    Raises:
        FileNotFoundError: When the executable is required and could not be found.
    """
    venv_executable_path = os.path.join(venv_dir, 'Scripts', executable)
    venv_executable = venv_executable_path if os.path.exists(venv_executable_path) else None

    if required and not venv_executable:
        raise FileNotFoundError(
                f'The virtual environment executable: {venv_executable_path} could not be found.')

    return venv_executable


def get_venv_python(venv_dir, required=True):
    """
    Return the Python executable inside a given virtual environment.

    Args:
        venv_dir (str): Path to the directory containing the virtual environment.
        required (bool): Whether to consider it a fatal error if the executable is not found.

    Returns:
        str or None: Full path to the Python executable inside the virtual environment. In case it cannot be
                     found, either an exception is raised or None is returned, depending on whether the
                     executable is required or not.

    Raises:
        FileNotFoundError: When the executable is required and could not be found.
    """
    return get_venv_executable(venv_dir=venv_dir, executable=os.path.basename(sys.executable),
            required=required)


def clear_venv(venv_dir):
    """
    Clear a virtual environment present in a given directory and restore it to a clean state. Note that this
    does not mean simply removing the entire folder, but rather uninstalls everything, leaving behind only
    those packages that are available in a fresh virtual environment (i.e., `pip` and `setuptools`).

    Args:
        venv_dir (str): Path to the directory containing the virtual environment.
    """
    vpython = get_venv_python(venv_dir, required=False)

    if not vpython:
        # Nothing to do.
        return

    # First get the list of all packages that should be uninstalled.
    reqs_file = tempfile.NamedTemporaryFile(delete=False, prefix='requirements.txt_')
    with reqs_file as fout:
        subprocess.check_call([vpython, '-m', 'pip', 'freeze'], stdout=fout)

    # Then actually remove them.
    subprocess.check_call([vpython, '-m', 'pip', 'uninstall', '-r', reqs.file.name, '-y'])

    # Clean up.
    os.remove(reqs_file)


def ensure_venv(venv_dir, python_version='system'):
    """
    Ensure the presence of a virtual environment in a given directory. If it already exists, nothing will be
    done. If it does not exist, the environment will be created and it will be ensured that the available
    `pip` and `setuptools` packages are updated to the latest version.
    """
    assert python_version == 'system', 'Currently only `system` Python version is supported.'

    if get_venv_python(venv_dir, required=False) is not None:
        # Nothing to do.
        return

    # Initialize the virtual environment.
    subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])

    vpython = get_venv_python(venv_dir)

    # Ensure recent versions of pip and setuptools.
    subprocess.check_call([vpython, '-m', 'pip', 'install', '--upgrade', 'pip>=19.0.0', 'setuptools>=41.0.0'],
            stdout=subprocess.DEVNULL)


def initialize_venv(venv_dir, reqs_file):
    """
    Initialize a virtual environment with default Python version, based on a given requirements file.

    Args:
        venv_dir (str): Path to a virtual environment.
        reqs_file (str): Path to the requirements file to be used.

    Raises:
        ValueError: If `reqs_file` does not exist.
    """
    if not os.path.exists(reqs_file):
        raise ValueError(f'Provided requirements file `{reqs_file}` does not exist.')

    if not os.path.exists(venv_dir):
        ensure_venv(venv_dir)

    subprocess.check_call([get_venv_python(venv_dir), '-m', 'pip', 'install', '-r', reqs_file])


def get_default_reqs_file():
    reqs_file = os.path.join(os.getcwd(), 'requirements.txt')
    if not os.path.exists(reqs_file):
        reqs_file = None
    return reqs_file


def main():
    parser = ArgumentParser(
            description='Create and initialize a virtual environment based on a requirements file.')
    parser.add_argument('venv_dir', nargs='?', default=os.path.join(os.getcwd(), '.venv'),
            help='Directory containing the virtual environment.')
    parser.add_argument('--requirement', '-r', default=get_default_reqs_file(),
            help='Optional path to the requirements file to be used.')
    parser.add_argument('--clear', '-c', default=False, action='store_true',
            help='If given, clear an already existing virtual environment before initializing it with '
                 'the provided requirements.')
    parser.add_argument('--force-remove', default=False, action='store_true',
            help='If given, fully remove an already existing virtual environment before initializing it '
                 'with the provided requirements.')
    args = parser.parse_args()

    if args.force_remove:
        # Let's open the discussion if somebody would like to actually fully remove the venv dir:
        assert False, '## Not implemented yet. Is it really needed?'
    elif args.clear:
        print(f'## Clearing venv at \'args.venv_dir\'...')
        clear_venv(venv_dir=args.venv_dir)

    if args.requirement:
        print(f'## Initializing venv at \'{args.venv_dir}\' using requirements file \'{args.requirement}\'...')
        initialize_venv(venv_dir=args.venv_dir, reqs_file=args.requirement)
    else:
        print(f'## Ensuring venv at \'{args.venv_dir}\'...')
        ensure_venv(venv_dir=args.venv_dir)

    print(f'## Virtual environment successfully initialized!')


if __name__ == '__main__':
    main()
