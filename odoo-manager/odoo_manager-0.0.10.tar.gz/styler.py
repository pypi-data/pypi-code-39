import os
import yapf
from yapf.yapflib.yapf_api import FormatFile


def filter_filename(filenames, root):
    """
    @return list
    """

    def _filter_filename(filename):
        full_filename = os.path.join(root, filename)
        rel_filename = os.path.relpath(full_filename)
        return filename.endswith(".py") and not any([rel_filename.startswith("."), rel_filename.startswith("_")])

    return filter(_filter_filename, filenames)


def format_directory(directory_path, styles_config):
    """
    @return None
    """
    for root, directories, filenames in os.walk(directory_path):
        filenames = filter_filename(filenames, root)

        for filename in filenames:
            full_filename = os.path.join(root, filename)
            rel_filename = os.path.relpath(full_filename)
            print("Formatting {}".format(rel_filename))

            try:
                formatted = FormatFile(full_filename, styles_config)[0]
                with open(full_filename, "w") as file:
                    file.write(formatted)
            except yapf.yapflib.verifier.InternalError as e:
                continue


styles_config = os.path.dirname(os.path.realpath(__file__)) + "/style.config"
current_directory = os.getcwd()
format_directory(current_directory, styles_config)
