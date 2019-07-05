""" these are the commands used in a notebook to setup and run the pipeline
"""

from . import config
from pipemaker.utils.filepath import Filepath
import os
import inspect
import types
from pipemaker.taskwrapper import TaskWrapper, pipeline

def make(*args, **kwargs):
    """ decorator that wraps a function to create a TaskWrapper """
    def inner(f):
        task = TaskWrapper(f, *args, **kwargs)
        #if no opath then cannot be turned into path
        if not hasattr(task, "opath"):
            return f
        # store so funcs can search for upstream funcs to make their inputs.
        pipeline.add(task)
        return task
    return inner

def make_all(module):
    """ create TaskWrappers for all functions in a module; and replace references in locals() with the TaskWrapper.
    """
    # update module (import module)
    for k, v in module.__dict__.items():
        if isinstance(v, types.FunctionType) and v.__module__ == module.__name__:
            setattr(module, k, make()(v))

    # update locals (from module import *)
    frame = inspect.currentframe()
    try:
        for k,v in frame.f_back.f_locals.items():
            if not k.startswith("_") and isinstance(v, types.FunctionType) and v.__module__ == module.__name__:
                frame.f_back.f_locals[k] =  make()(v)
    finally:
        del frame

def cleanup(datapath):
    """ cleanup all temp folders
    """
    fp = Filepath(datapath)
    g = fp.fs.glob(f"{fp.path}/**/temp/")
    folders = "\n".join([f.path for f in g])
    if not folders:
        print("no temp folders found")
        return
    r = input(f"Will delete the following folders. Please type y to confirm.\n{folders}\n")
    if r=="y":
        g.remove()
    else:
        print("cancelled deletion")

def getUrl(name):
    """ return Filepath from name
    :filepath can be varname, varname.pkl or url
    """
    # varname
    if name.find("/")<0:
        # default extension
        if len(os.path.splitext(name))==1:
            name = f"{name}.pkl"
        config.pathvars.subpath = name
        return config.path.format(**config.pathvars)
    return name

def load(name):
    """ return contents
    """
    url = getUrl(name)
    return Filepath(url).load()

def save(obj, name):
    """ save obj to filename or url """
    url = getUrl(name)
    Filepath(url).save(obj)