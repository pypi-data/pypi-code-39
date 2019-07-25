from os import path, mkdir
import sys
from jinja2 import Environment, PackageLoader

def package_init(packspec, overwrite=False):
    """Initializes the generated package folder structure, if it doesn't already
    exist.

    Args:
        packspec (AttrDict): specification for the overall application, which
            includes path information for the generated component.
        overwrite (bool): when True, overwrite the package file if it already
            exists.

    Returns:
        tuple: `(root, coderoot)`, where root is the repository root folder,
        and `coderoot` is the sub-directory where python code is stored.
    """
    root = path.abspath(path.expanduser(packspec.root))
    #Make sure that the repository root path is in the python path for dynamic
    #imports of the generated package.
    if root not in sys.path:
        sys.path.insert(0, root)
    coderoot = path.join(root, packspec.name)

    setup = path.join(root, "setup.py")
    if path.isfile(setup) and not overwrite:
        return root, coderoot

    if not path.isdir(root): # pragma: no cover
        mkdir(root)
    if not path.isdir(coderoot): # pragma: no cover
        mkdir(coderoot)
    init = path.join(coderoot, "__init__.py")

    env = Environment(loader=PackageLoader('datakeeper', 'templates'))
    t_setup = env.get_template("setup.py")
    t_init = env.get_template("init.py")

    with open(setup, 'w') as f:
        f.write(t_setup.render(**packspec))
    with open(init, 'w') as f:
        f.write(t_init.render(**packspec))

    return root, coderoot

def component_write(packspec, compspec, overwrite=False):
    """Writes the python code file for the specified component specification so
    that a :class:`flask.Blueprint` can be created via direct import.

    Args:
        packspec (AttrDict): specification for the derived package, which
            includes path information for the generated component.
        compspec (AttrDict): component specification to create.
        overwrite (bool): when True, overwrite the module file if it already
            exists.
    """
    root, coderoot = package_init(packspec, overwrite)
    target = path.join(coderoot, "{}.py".format(compspec.name))
    if path.isfile(target) and not overwrite:
        return

    env = Environment(loader=PackageLoader('datakeeper', 'templates'))
    template = env.get_template("component.py")
    cpspec = compspec.copy()
    cpspec["package"] = packspec

    with open(target, 'w') as f:
        f.write(template.render(**cpspec))
