import os
import hashlib


def get_version():
    root = os.path.dirname(__file__)
    hasher = hashlib.sha256()
    for directory, _, files in os.walk(root):
        for filename in files:
            with open(os.path.join(directory, filename), "rb") as file:
                hasher.update(file.read())
    return hasher.hexdigest()


version = get_version()
