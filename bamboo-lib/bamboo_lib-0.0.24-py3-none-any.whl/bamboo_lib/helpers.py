import os
import string
import random
import itertools


from bamboo_lib.connectors.models import Connector


def grab_parent_dir(file_starting_point):
    """Given a string indicating a system file path, build a path to the parent directory.

    :param file_starting_point: file path string from which to compute the parent directory.
    :return: String to the absolute path of the file_starting_point parent folder
    """
    return os.path.abspath(os.path.join(file_starting_point, os.pardir))


def grab_connector(file_starting_point, cname):
    """ Given a filepath and connector name, retrieves and builds the
    connector configuration object.

    :param file_starting_point: filepath from which to base the search for the conns.yaml file.
    :param cname: name of the connector to look up
    :return: Connector object
    """
    # try local file first then fall back to global
    par_dir = os.path.abspath(os.path.join(file_starting_point, os.pardir))
    local_conn_path = os.path.join(par_dir, "conns.yaml")
    # source = local_conn_path.get(cname, global_conn_path.get(cname))
    try:
        connector = Connector.fetch(cname, open(local_conn_path))
    except ValueError:
        BAMBOO_FALLBACK_CONNS = os.environ.get("BAMBOO_FALLBACK_CONNS")
        # TODO allow env var to customize default fallback config path
        global_conn_path = os.path.expanduser(os.path.expandvars(BAMBOO_FALLBACK_CONNS))
        connector = Connector.fetch(cname, open(global_conn_path))
    return connector


def random_char(num_characters):
    """ Returns a string of num_characters random ASCII characters.

    :param num_characters: Integer representing the number of characters to appear in the output.
    :return: String
    """
    return ''.join(random.choice(string.ascii_letters) for x in range(num_characters))


def dict_product(dicts):
    """ Given a dictionary of lists, returns a list of dictionaries containing the cross-product
    of associated items.

    :param dicts: Dictionary mapping names to lists
    :return: list of dict
    """
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))


def expand_path(my_path_str):
    """ Given a string path, expand and replace any matching environment variables or user references.
    return os.path.expanduser(os.path.expandvars(my_path_str))

    :param my_path_str: String representing the target path
    :return: String representing the target path with any environment variables or user references.
    """
    return os.path.expanduser(os.path.expandvars(my_path_str))
