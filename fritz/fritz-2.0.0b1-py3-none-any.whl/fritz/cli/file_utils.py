"""Helpers for dealing with the filesystem."""

import os
import fileinput


def find_line_search_term(path, search_term):
    with open(path) as f:
        for i, line in enumerate(f):
            if search_term in line:
                return i

    return None


def insert_code_before(tag_to_insert_before, code_to_insert, file_to_write):
    """Insert the code before the found string.

    Args:
        tag_to_insert_before: the text to search for.
        code_to_insert: insert the code
            before the found text.
        file_to_write: the file to write to.
    """

    content = ""
    for line in fileinput.input(file_to_write):
        if tag_to_insert_before in line:
            content += code_to_insert
        content += line
    with open(file_to_write, "w+") as file:
        file.write(content)


def insert_code_after_line(file_path, line_number, code):
    """Insert code after the specified line.

    Args:
        tag_to_insert_before: the text to search for.
        code_to_insert: insert the code
            before the found text.
        file_to_write: the file to write to.
    """

    with open(file_path) as f:
        contents = f.readlines()
        contents.insert(line_number + 1, code)

    with open(file_path, "w") as f:
        f.write("".join(contents))


def is_text_in_file(text_to_find, file_path):
    """Find the text in all the file

    text_to_find: the text to find.
        file_path: the path to the file to search through.

    Returns:
        True or False if the text is in the file
    """

    return is_text_in_files(text_to_find, [file_path])


def is_text_in_files(text_to_find, file_paths):
    """Find the text in all the files.

    Args:
        text_to_find: the text to find.
        file_path: the path to the file to search through.

    Returns:
        True or False if the text is in the file
    """

    for file_path in file_paths:
        if find_text_in_file(text_to_find, file_path):
            return True
    return False


def find_text_in_file(text_to_find, file_path):
    """Find a certain text string in the file.

    Args:
        text_to_find: the text to find.
        file_path: the path to the file to search through.

    Returns:
        the specific line the text was on (grep).
    """
    with open(file_path) as file:
        datafile = file.readlines()
        for line in datafile:
            if text_to_find in line:
                return line

    return None


def find_all(name, path="."):
    """Find the all occurrences in a directory

    Args:
        name: name of the file to find
        path: directory to search through

    Returns:
        the file paths found with the text name
    """
    result = []
    for root, _, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find(name, path="."):
    """Find the first occurrence in a directory

    Args:
        name: name of the file to find
        path: directory to search through

    Returns:
        the path of the found file or none
    """
    for root, _, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None
