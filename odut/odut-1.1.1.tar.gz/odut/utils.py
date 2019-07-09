# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import doctest
import re
import itertools
# import logging
from shutil import rmtree

# __manifest__ file: 
# search for pattern:
# 'depends' : ['base_setup', 'product', 'analytic', 'portal', 'digest'],
PAT = re.compile(r"'depends'\s*?:\s*?\['.*\]")

def get_target_path(base_path, target):
    '''Get addon path, Pathlike object.

    Usage:
    >>> get_target_path('.', 'odut.txt')
    PosixPath('odut.txt')

    or WindowsPath('odut.txt') if using a windows machine.
    ''' 
    project_path = Path(base_path) # accept relative path.
    # Path(x)
    return Path(target) if (lambda target: Path(target).name in project_path.iterdir()) else None

D = []
def get_dependencies(file):
    """Get dependencies for a single file using regex.

    Usage:
    >>> get_dependencies(Path('./account_test/__manifest__.py'))
    [['base_setup', 'product', 'analytic', 'portal', 'digest']]
    """
    with open(file, 'r') as fp:
        f = fp.read()
        match = PAT.search(f)
        if match:
            d = match.group().split(':')[1].strip(' []').split(",")
            d = list(map(lambda x: x.strip(" '"), d))
            D.append(d)


def get_modules_dependencies(modules=None, file=None, base_dir=False):
    '''Receive a list of modules and return their dependencies. 

    :parms: modules: Iterable
    :returns: list of module names
    :rtype: List str

    Usage:

    '''
    work_dir = Path(base_dir) if base_dir else Path('.')
    if file:
        # read the modules for the file.
        with open(file, 'r') as f:
            l = f.readline()
            modules = list(map(lambda x: x.strip('\n'), l.split(',')))

    # covert to list of path object.
    addon_module_paths = [x for x in work_dir.iterdir() if x.is_dir()]
    # print(addon_module_paths)
    # first, make sure all the modules are in the add-ons.
    for m in modules: # size around 10.
        addon_path = Path(work_dir) / m
        # print(addon_path)
        if addon_path not in addon_module_paths:
            raise ValueError(f"{m} is not a valid module")
        try:
            get_dependencies(addon_path / '__manifest__.py')
        except FileNotFoundError as e:
            # logging.exception(e)
            print(e)


def get_all_modules_path(base_dir):
    '''get all the addons within the basedir.
    '''
    work_dir = Path(base_dir) if base_dir else Path('.')
    return set([x for x in work_dir.iterdir() if x.is_dir()])

def resolve_dependencies(modules=None, file=None, base_dir=None):
    """Delete unncessary modules.
    """
    get_modules_dependencies(modules=modules, file=file, base_dir=base_dir)
    # print(D)
    ds = itertools.chain(*D)
    s = set(list(ds))
    s.update(set(modules))

    addon_paths = get_all_modules_path(base_dir=base_dir)
    # print(addon_paths)
    sn = set(map(lambda x: Path(base_dir) / x, s))
    res = addon_paths - sn

    pat = re.compile('l10')
    for i in res:
        print(str(i))
        # remove all the dependencies except the i10n 
        if not pat.search(str(i)):
            rmtree(i)
 

# if __name__ == "__main__":
#     pass
    # import doctest
    # doctest.testmod()
    # print(Path('~/'))
    # get_modules_dependencies(modules=['account', 'crm', 'delivery'],base_dir='/Users/yinet/Desktop/odoo/odoo/addons')
    # s = resolve_dependencies(modules=['account', 'crm', 'delivery'],base_dir='/Users/yinet/Desktop/odoo2/addons')
