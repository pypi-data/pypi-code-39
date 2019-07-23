from os.path import join
import sys


def load_sql(dir: str, name: str) -> str:
    """
    Wrapper to load SQL from a director and name of file without extension specified (assumes .sql)
    :param dir: Directory Path
    :param name: File Name Without Extension (.sql only)
    :return: string object
    """
    try:
        sql_file = join(dir, '{}.sql'.format(name))
        with open(sql_file) as f_in:
            return f_in.read()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(e)


def subfolder_path(path: str, subpath) -> str:
    """
    Wrapper to easily build a path using basepath and a string/list of subpaths
    :param path: basepath
    :param subpath: Can be a path (as string) or list of paths.
    :return: full_path built using basepath and subpaths
    """
    try:
        if isinstance(subpath, str):
            full_path = join(path, subpath)
        elif isinstance(subpath, list):
            full_path = join(path, "/".join(subpath))
        else:
            full_path = path

        return full_path
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(e)
