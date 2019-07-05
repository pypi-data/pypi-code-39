import inspect
from graphviz import Digraph
from copy import deepcopy

from .utils.dotdict import dotdict
from .utils.filepath import Filepath
from .task import Task
from .pipeline import Pipeline

from . import config

import logging
log = logging.getLogger()

pipeline = Pipeline()

if config.queue:
    from pipemaker.worker.taskq import Taskq
    taskq = Taskq()

class TaskWrapper:
    """
    Wraps a function with features required for the pipeline

    run
    * format input and output filepaths using config
    * return output if exists
    * submit func and any upstream tasks for execution

    utils
    * force rerun
    * display upstream pipeline using graphviz
    """
    def __init__(self, func, ipaths=None, opath=None):
        """
        :param func: function to wrap
        :param ipaths: dict(param=path)
        :param opath: path

        paths are fstrings in format filesystem|path or path
        if ipath or opath not specified then uses config.path
        placeholders are filled at runtime from config.pathvars
        """
        self.func = func
        # function parameters. set manually if needed for upstream funcs.
        self.params = dotdict()

        # optional input paths
        self.ipaths = dotdict()
        if ipaths:
            self.ipaths = dotdict(ipaths)

        # output path
        if opath:
            # parameter
            self.opath = opath
        else:
            # return annotation
            sig = inspect.signature(func)
            if sig.return_annotation!=inspect._empty:
                self.opath = sig.return_annotation

            # function name
            elif self.func.__name__.startswith("make_"):
                self.opath = self.func.__name__[len("make_"):]

        # set save=False to allow function to manage saving
        self.save = True

    def __repr__(self):
        params = ",".join(str(p) for p in inspect.signature(self.func).parameters.values())
        return f"{self.func.__name__}({params})->{self.parse_output()}"

    def parse_output(self):
        """ path to output file """

        # global config
        if self.opath in config.fixedpaths:
            path = config.fixedpaths[self.opath]
        else:
        # default fstring
            pathvars = deepcopy(config.pathvars)
            pathvars.subpath = self.opath
            path = config.path.format(**pathvars)
        return Filepath(path)

    def parse_inputs(self, *args, **kwargs):
        """ return input params and filepaths

        :param args:    args passed to function at runtime
        :param kwargs:  kwargs passed to function at runtime
        :return:        dict of name=value where value is parameter value or filepath
        """
        inputs = dict()
        for i, (k, v) in enumerate(inspect.signature(self.func).parameters.items()):

            # run_time function parameter e.g. myfunc(input1=2)
            if i < len(args):
                inputs[k] = args[i]
            elif k in kwargs:
                inputs[k] = kwargs[k]
            # task parameter e.g. mytask.param.input1=2
            elif k in self.params:
                inputs[k] = self.params[k]
            # global parameter
            elif k in config.params:
                inputs[k] = config.params[k]
            # compile_time default e.g. def myfunc(input1=2)
            elif v.default != inspect._empty:
                inputs[k] = v.default

            # path can be fs_url|path; or path relative to current folder
            else:
                # task parameter
                if k in self.ipaths:
                    path = self.ipaths[k]
                # global config
                elif k in config.fixedpaths:
                    path =config.fixedpaths[k]
                # default fstring
                else:
                    pathvars = deepcopy(config.pathvars)
                    pathvars.subpath = v
                    path = config.path.format(**pathvars)
                inputs[k] = Filepath(path)

        return inputs

    def reset(self):
        """ remove output to force step to rerun """
        try:
            self.parse_output().remove()
        except FileNotFoundError:
            pass
        return self

    def __call__(self, *args, **kwargs):
        """ called in same way as underlying function would be called e.g. make_something(5, a=3) """
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """ fix input/output locations. submit upstream and func for execution
        params are filled from args/kwargs; config.params; filepath; upstream task
        """
        if config.pathvars.job is None:
            raise Exception("Set config.pathvars.job which is used for file locations")

        # if output already available then return it
        self.output = self.parse_output()
        if self.output.exists():
            self.outdata = self.output.load()
            return self.outdata

        # get input params/filepaths; and determine upstream tasks
        self.inputs = self.parse_inputs(*args, **kwargs)
        upstream = {k: v for k, v in self.inputs.items() if isinstance(v, Filepath) and not v.exists()}
        uptasks = {k:pipeline.find(v) for k,v in upstream.items()}

        # fail if missing upstream functions
        missing = [k for k,v in uptasks.items() if v is None]
        if missing:
            raise Exception(f"Missing input values for {missing}")

        # call upstream tasks
        for k,v in uptasks.items():
            self.inputs[k] = v.run()

        # execute
        task = Task(self.func, self.inputs, self.output, self.save)
        if config.queue:
            taskq.put(task)
        else:
            return task.run()


    def show(self, g=None, parents=False):
        """ return graphviz display of upstream pipeline
        :param g: existing graph. passed recursively to show parents
        :param parents: False shows funcs that need to be run. True shows all upstream funcs
        """
        # create graph on first call
        if g is None:
            g = Digraph(strict=True, comment=f'{self.func.__name__} pipeline')
            log.info(f"Pipeline to produce {self.parse_output()}")

        # display formats
        func_style = dict(shape="oval", style="filled", fillcolor="lightgrey")
        exists_style = dict(shape="folder", height=".1", width=".1", style="filled", fillcolor="lightgreen")
        missing_style = dict(shape="folder", height=".1", width=".1", style="")
        pexists_style = dict(shape="box", style="filled", fillcolor="lightgreen")
        pmissing_style = dict(shape="box", style="")

        # function
        g.node(self.func.__name__, **func_style)

        # inputs
        inputs = self.parse_inputs()
        for k,v in inputs.items():
            if isinstance(v, Filepath):
                if v.exists():
                    g.node(k, **exists_style)
                    g.edge(k, self.func.__name__)
                    if parents:
                        pw = pipeline.find(v)
                        if pw is not None:
                            pw.show(g, parents)
                else:
                    upstream = pipeline.find(v)
                    if upstream:
                        # no file but a task can create it
                        upstream.show(g, parents)
                        g.edge(k, self.func.__name__)
                    else:
                        # no parameter. no file. no task to create it.
                        g.node(k, **pmissing_style)
                        g.edge(k, self.func.__name__)
            else:
                # supplied parameter
                g.node(k, **pexists_style)
                g.edge(k, self.func.__name__)

        # output
        output = self.parse_output()
        if output.exists():
            g.node(output.varname, **exists_style)
        else:
            g.node(output.varname, **missing_style)

        g.edge(self.func.__name__, output.varname)

        return g