import os
from typing import Dict
from cnvrg.helpers.hash_helper import hash_file
import mimetypes

def get_file_props(file: str, working_dir: str) -> Dict:
    '''

    :param file:
    :param working_dir:
    :return: {relative_path, file_name, file_size, content_type, sha1}
    '''
    abs_file_path = os.path.realpath(os.path.join(working_dir, file))
    relative_path = os.path.relpath(file, working_dir)
    size = os.path.getsize(abs_file_path)
    file_name = os.path.basename(abs_file_path)
    content_type = mimetypes.MimeTypes().guess_type(abs_file_path)[0] or "text/plain"
    return {
        "relative_path": relative_path,
        "file_name": file_name,
        "file_size": size,
        "content_type": content_type,
        "sha1": hash_file(abs_file_path, raw=True)
    }