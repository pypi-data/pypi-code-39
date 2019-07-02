"""
amt-save -- Artifact Management Tool Reader

amt is a Tool for managing software artifacts

It defines classes_and_methods and a command line interface

@author:     Kenneth E. Bellock

@copyright:

@contact:    ken@bellock.net

"""
import os
import sys
import tempfile
import shutil
from filecmp import dircmp
import yaml

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_PATH), 'meta'))
from meta import MetaDict
from meta import MetaList
yaml.add_representer(MetaDict,
                     lambda dumper, data: dumper.represent_mapping(
                         'tag:yaml.org,2002:map', data.items()))
yaml.add_representer(MetaList,
                     lambda dumper, data: dumper.represent_sequence(
                         'tag:yaml.org,2002:seq', data))

__all__ = ['save']


def _d(path, data):
    for key, value in data.items():
        try:
            with open(os.path.join(path, value._file), 'w') as f_obj:
                f_obj.write(yaml.dump(value, default_flow_style=False))
        except:
            newpth = os.path.join(path, key)
            if not os.path.isdir(newpth):
                os.makedirs(newpth)
            save(newpth, value)


def _d2(dcmp):
    for f in dcmp.left_only:
        if os.path.isdir(f):
            shutil.rmtree(f)
        elif os.path.isfile(f):
            os.remove(f)
    for fname in list(set(dcmp.right_only + dcmp.diff_files)):
        f = os.path.join(dcmp.right, fname)
        if os.path.isfile(f):
            relpath = os.path.relpath(f, dcmp.right)
            target = os.path.join(dcmp.left, relpath)
            target_dirname = os.path.dirname(target)
            if not os.path.isdir(target_dirname):
                os.makedirs(target_dirname)
            shutil.copy2(f, target)
        elif os.path.isdir(f):
            shutil.copytree(os.path.join(dcmp.right, fname),
                            os.path.join(dcmp.left, fname))
    for key, value in dcmp.subdirs.items():
        _d2(value)


def save(path, data, header=None, footer=None):
    """
    Save an artifacts tree to a file or directory location.

    Args:
        path (str): The file or directory location to save the artifacts tree
                    to.
        data (str or list or dict): The artifacts tree.
        header (:obj:`str`, optional): Header for artifacts files.
        footer (:obj:`str`, optional): Footer for artifacts files.
    """
    if path.lower().endswith('.yaml'):
        write_data = data.copy()
        f_obj = open(path, 'w')
        if header:
            f_obj.write(header)
        f_obj.write(yaml.dump(write_data, default_flow_style=False))
        if footer:
            f_obj.write(footer)
        f_obj.close()
    else:
        tmp = tempfile.mkdtemp()
        _d(tmp, data)
        _d2(dircmp(path, tmp))
        shutil.rmtree(tmp)
