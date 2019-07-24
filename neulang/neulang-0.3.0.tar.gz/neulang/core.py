#! /usr/bin/env python3
"""

"""


import traceback as tb

from ast import *
from os.path import exists as op_exists, join as op_join, isfile as op_isfile
import re
import sys

try:
    import astor

except:
    pass

from neulang.omp import OMP
from neulang.resolvers import Resolver
from neulang.pubsub import PubSub


if not sys.version_info[:2] == (3, 7):
    msg = "Neulang was created and tested with Python 3.7, but detected {}. YMMV.".format(
        ".".join([str(n) for n in sys.version_info[:3]])
    )
    import warnings

    warnings.warn(msg, RuntimeWarning)


class AttribProxy:
    """Generate access via attributes"""

    # TODO: move to utils

    def __init__(self, data):
        self._data = data
        # self._func = func
        # self._args = args
        # self._kwds = kwds
        return

    def __getattr__(self, attr):
        data = self._data
        if isinstance(data, dict):
            return data[attr]
        if callable(data):
            return data(attr)
        raise AttributeError("Unable to process {attr}")


class Neulang:
    def __init__(self, *args, **kwds):
        ns = kwds.get("namespace", None)
        self._ns = ns = ns if isinstance(ns, dict) else {}
        self._ps = ps = PubSub()
        self._resolver = Resolver(parent=self, pubsub=ps)
        self._ast = None
        self._src = None
        self._latest = None
        self._org_path = None
        ns["include"] = self.load_module
        ns["__PUBSUB__"] = ps
        return

    def load_astir(self, af=""):
        ns = {}
        if not exists(af):
            return
        am = self.load(af)
        am = compile(am, af, "exec")
        exec(am, ns)
        ap = AttribProxy(ns)
        return ap

    def load(self, path):
        if not op_exists(path):
            raise OSError(f"{path} not found")
        success = None

        mod = open(path).read()

        try:
            success = self.loads(mod, sf=path)

        except AssertionError as e:
            tb.print_exc()
            print("\n\nPlease report this error to the developer")
            return False

        except Exception as e:
            tb.print_exc()
            return False
        return success

    def loads(self, text, sf="<module>"):
        """Convert org text to AST object"""
        ompo = OMP()
        ompo.loads(text, self._org_path)

        try:
            ast = self._resolver.resolve(ompo.tree)

        except Exception as e:
            raise
        assert isinstance(
            ast, AST
        ), f'expected an AST object but got "{ast.__class__.__name__}" object instead'
        self._ast = ast
        self._src = sf
        self._latest = False
        return True

    def eval(self, mode="exec"):
        if self._latest:
            return
        rv = None

        if mode == "exec":
            exec(compile(self._ast, self._src, "exec"), self._ns)

        elif mode == "eval":
            ast = self._ast
            if isinstance(ast, Module):
                ast = ast.body[0]
                ast = Expression(ast.value if isinstance(ast, Expr) else ast)
            rv = eval(compile(ast, self._src, "eval"), self._ns)
            self._ns["_"] = rv
        self._latest = True
        return rv

    def reset(self):
        self._ast = self._ns = None
        self._latest = True
        return

    def org_path(self, op):
        if not op or not isinstance(op, list):
            return False
        self._org_path = op
        return True

    @property
    def ns(self):
        return self._ns

    def update_namespace(self, *r_list, **a_dict):
        if (r_list and not all([i.isidentifier() for i in r_list])) or (
            a_dict and not all([k.isidentifier() for k in a_dict.keys()])
        ):
            raise NameError("All items and keys must be valid names")
        ns = self._ns

        for name in r_list:
            if name in ns:
                del ns[name]

        for k, v in a_dict.items():
            ns[k] = v
        return True

    def to_py(self):
        if "astor" not in globals():
            raise ImportError(
                'Cannot convert to py as astor module not found. Run "pip install astor" and try again.'
            )
        ast = self._ast
        if not ast:
            raise ValueError("No source code loaded.")
        py = astor.to_source(ast)
        return py

    def load_module(self, name, package=None):
        res = False
        f_name = "{}.neu".format(op_join(".", name))

        if not "." in name and op_exists(f_name):
            res = self.load(f_name)
            return res
        n_parts = name.split(".")
        s_paths = sys.path  # TODO: get path from ns
        assert all([isinstance(p, str) for p in s_paths]), "All paths must be strings"
        if not "" in s_paths:
            s_paths.insert(0, "")
        checked = []
        m_paths = []

        for path in s_paths:
            if not path:
                path = "."
            if path in checked:
                continue
            checked.append(path)
            if op_exists(op_join(path, n_parts[0], "__init__.neu")):
                success = self._name_to_paths(path, n_parts[:], m_paths)
                if success and m_paths:
                    m_paths = m_paths[::-1]
                    break
        else:
            raise ModuleNotFoundError(f'Cannot resolve "{name}"')

        for mp in m_paths:
            try:
                res = self.load(mp)
                self.eval()

            except Exception as e:
                raise ImportError(f'unable to process "{mp}"; {e.args[0]}')
        return res

    def _name_to_paths(self, path, n_parts, m_paths, p_parts=None):
        if not p_parts:
            p_parts = []
        np = n_parts.pop(0)
        p_parts.append(np)
        nfs = [
            op_join(path, *p_parts, "__init__.neu"),
            "{}.neu".format(op_join(path, *p_parts)),
        ]
        if not (op_isfile(nfs[0]) or op_isfile(nfs[1])):
            return False

        if not n_parts:
            if op_exists(nfs[1]):
                m_paths.append(nfs[1])
            if op_exists(nfs[0]):
                m_paths.append(nfs[0])
            return True
        success = self._name_to_paths(path, n_parts, m_paths, p_parts)
        if success:
            assert op_exists(nfs[0]), f'"{nfs[0]}" not found'
            m_paths.append(nfs[0])
        return success

    def sub(self, *args, **kwds):
        return self._ps.sub(*args, **kwds)
