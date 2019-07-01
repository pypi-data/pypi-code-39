import collections
import configparser
import fnmatch
import pathlib
import typing


# Structure that identifies the configuration.
Config = collections.namedtuple('Config', [
    'ignores',
])

# Structure that identifies config types what can be parsed.
Configfile = collections.namedtuple('Configfile', [
    'filename',
    'option',
    'section',
])

# Types of config files for parsing.
CRLINT_CONFIG = Configfile(filename='.crlintrc', option='patterns', section='ignore')
SETUP_CONFIG = Configfile(filename='setup.cfg', option='patterns', section='crlint')


def scantree(work_path: str) -> typing.Iterator:
    """Directory recursive scanning.

    Directory recursive scanning for getting all files
    paths. This method used to walk directory recursively
    and return all file paths to this directory.

    Arguments:
        root_path: a provided path to start scanning.

    Yields:
        An absolute path to the current file.
    """
    for path in pathlib.Path(work_path).glob('**/*'):
        if path.is_file():
            yield path.absolute()


def is_excluded(file_path: str, exclusions: typing.List[str]) -> bool:
    """Check file path to match ignore pattern.

    Excludes file paths if they match user-submitted
    exclusion patterns. This method used to filtering
    available file paths by providing ignore patterns.

    Arguments:
        file_path: provided path to file for checking.
        exclusions: a files ignore pattern.

    Returns:
        An indicator for current file ignores it or not.
    """
    return any(
        fnmatch.fnmatch(file_path, exclusion)
        for exclusion in exclusions
    )


def get_config(work_path: str) -> configparser.ConfigParser:
    """Load configuration file and parse it.

    Depending on what config file (setup.cfg or crlitrc)
    get actual sections. If there are both files setup.cfg
    will be primarily parsed. This method use to load and
    parse configuration file.

    Arguments:
        work_path: a root directory for running a check.

    Raises:
        FileNotFoundError: raises if file wasn't found.

    Returns:
        A parsed the configuration file.
    """
    work_path = pathlib.Path(work_path)

    # Find the configuration file by priority.
    config_file = None
    for config in (SETUP_CONFIG, CRLINT_CONFIG):
        if work_path.joinpath(config.filename).exists():
            config_file = config
            break

    # Raise an error in case of not finding at least one config.
    if config_file is None:
        raise FileNotFoundError('Cannot found {0} or {1} config'.format(
            CRLINT_CONFIG.filename,
            SETUP_CONFIG.filename,
        ))

    # Loading the founded configuration file.
    config = configparser.ConfigParser()
    config.read(work_path.joinpath(config_file.filename))

    config_exclusion_patterns = [
        pattern.strip()
        for pattern in config.get(config_file.section, config_file.option).split(',')
    ]
    return Config(ignores=config_exclusion_patterns)
