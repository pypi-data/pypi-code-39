"""
Python keywords made callable.
"""


from importlib import import_module


class CalleeException(Exception):
    pass


class BreakException(CalleeException):
    pass


class ContinueException(CalleeException):
    pass


class Callee:
    def __init__(self, *, namespace=None):
        if not isinstance(namespace, (dict, type(None))):
            raise ValueError('"namespace" must be a dict or None')
        self._vars = namespace or {}
        return

    @property
    def ns(self):
        return self._vars

    def x_setv(self, *names, value=NotImplemented):
        # NB: could blow up if someone actually wants to set NotImplemented
        names = list(names)
        if value is NotImplemented and len(names) > 1:
            value = names.pop(-1)
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise NameError(f"names must be valid identifier(s)")
        if value is NotImplemented:
            raise ValueError("no value to set")
        for name in names:
            self._vars[name] = value
        return value

    def x_getv(self, *names):
        if not names:
            raise NameError("no name to get")
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise NameError(f"names must be valid identifier(s)")
        values = []
        vars = self._vars

        for name in names:
            if name not in vars:
                raise NameError(f'name "{name}" is not defined')
            values.append(vars[name])
        return tuple(values) if len(values) > 1 else values[0]

    def x_delv(self, *names):
        if not names:
            raise NameError("no names to delete")
        if not all([isinstance(n, str) and n.isidentifier() for n in names]):
            raise ValueError("must be valid identifier(s)")
        values = []
        vars = self._vars

        for name in names:
            if not name in vars:
                raise NameError(f'name "{name}" is not defined')
            values.append(vars.pop(name))
        return values

    def x_if(self, test, body, orelse=None, **ctx):
        if not orelse:

            def orelse(**ctx):
                return retv

        if isinstance(test, str):

            def test(**ctx):
                return eval(test, globals(), ctx)

        if not all([callable(f) for f in [test, body, orelse]]):
            raise Exception("All must be callables")
        retv = None

        if test(**ctx):
            retv = body(**ctx)

        else:
            retv = orelse(**ctx)
        return retv

    def x_for(self, target, iter_, body, orelse=None, **ctx):
        if (
            not isinstance(target, str)
            or not target.isidentifier()
            and not all([s.isidentifier() for s in target.split(", ")])
        ):
            raise ValueError(
                '"target" must be a string identifier or comma separated identifiers'
            )
        iter(iter_)
        if orelse is None:

            def orelse(**ctx):
                return retv

        if not all([callable(f) for f in [body, orelse]]):
            raise ValueError("All must be callables")
        locs = {
            "iter_": iter_,
            "body": body,
            "orelse": orelse,
            "retv": None,
            "ctx": ctx,
        }

        f_loop = f"""
for {target} in iter_:
    try:
        retv = body({target}, **ctx)

    except BreakException:
        break

    except ContinueException:
        continue

else:
    retv = orelse(**ctx)"""
        exec(f_loop, globals(), locs)
        return locs.get("retv")

    def x_while(self, test, body, orelse=None, **ctx):
        if orelse is None:

            def orelse(**ctx):
                return retv

        if isinstance(test, str):
            test_str = test

            def test(**ctx):
                return eval(test_str, globals(), ctx)

        if not all([callable(f) for f in [test, body, orelse]]):
            raise Exception("All must be callables")
        retv = None

        while test(**ctx):
            try:
                retv = body(**ctx)

            except BreakException:
                break

            except ContinueException:
                continue

        else:
            retv = orelse(**ctx)
        return retv

    def x_break(self, *args, **kwds):
        raise BreakException()

    def x_continue(self, *args, **kwds):
        raise ContinueException()

    def x_do(self, *funcs, **ctx):
        if not funcs:
            return None
        funcs = [f for f in funcs]
        if isinstance(funcs[-1], dict) and not ctx:
            ctx = funcs.pop(-1)
        if not all([callable(f) for f in funcs]):
            raise ValueError("Must all be callables")
        retv = None

        for func in funcs:
            retv = func(**ctx)
            ctx["return"] = retv
        return retv

    def x_import(self, *names, packages=None):
        if not names:
            raise NameError("no names to import")
        if packages is None:
            packages = [None] * len(names)
        if isinstance(packages, str):
            packages = [packages]
        if not (
            isinstance(packages, (list, tuple))
            and len(packages) == len(names)
            and all([isinstance(p, (str, type(None))) for p in packages])
        ):
            raise ImportError(
                '"packages" must be a string or list of strings for packages corresponding to given names'
            )
        mods = []

        for name, package in zip(names, packages):
            mods.append(import_module(name, package))
        return tuple(mods) if len(mods) > 1 else mods[0]

    def x_with(self, *items, body=None, **ctx):
        if not items:
            raise ValueError("no items to create context")
        items = list(items)
        if body is None:
            body = items.pop(-1)
        if (
            len(items) == 2
            and callable(items[0])
            and isinstance(items[1], (str, type(None)))
        ):
            items = [items]
        if all(
            [
                (
                    isinstance(i, (list, tuple))
                    and len(i) == 2
                    and callable(i[0])
                    and isinstance(i[1], (str, type(None)))
                )
                for i in items
            ]
        ):
            items = {i[1]: i[0] for i in items}
        if not (
            isinstance(items, dict)
            and all([isinstance(n, (str, None)) for n in items.keys()])
            and all([callable(i) for i in items.values()])
        ):
            raise ValueError("Bad items format")
        if not callable(body):
            raise ValueError('"body" must be callable')
        header = ", ".join(
            [f"{v.__name__}()%s" % (f" as {k}" if k else "") for k, v in items.items()]
        )
        w_args = ", ".join([k for k in items if isinstance(k, str)])
        if w_args:
            w_args += ", "
        e_ctx = {c.__name__: c for c in items.values()}
        locs = {"body": body, "retv": None, "ctx": ctx, **e_ctx}
        w_ctx = f"""
with {header}:
    retv = body({w_args}**ctx)
        """
        exec(w_ctx, globals(), locs)
        return locs.get("retv")

    def x_class(self, name, attrdict, bases=None, decorators=None):
        retv = None
        if not (
            isinstance(attrdict, dict)
            and all([isinstance(k, str) and k.isidentifier() for k in attrdict])
        ):
            raise ValueError("Class attrdict must be a dict of attribs")
        if bases is None:
            bases = ()
        if decorators is None:
            decorators = []
        cls = type(name, bases, attrdict)

        for d in decorators:
            cls = d(cls)
        return cls

    def x_try(self, body, *handlers, orelse=None, finalbody=None, **ctx):
        if not callable(body):
            raise ValueError('"body" must be callable')
        if not (
            isinstance(handlers, (list, tuple))
            and all(
                [
                    (
                        isinstance(h, (list, tuple))
                        and len(h) == 2
                        and (
                            isinstance(h[0], Exception)
                            or hasattr(h[0], "with_traceback")
                        )
                        and callable(h[1])
                    )
                    for h in handlers
                ]
            )
        ):
            raise ValueError(
                '"handlers" must be a list or tuple of exception, callable handler lists/tuples'
            )
        if orelse is None:

            def orelse(**ctx):
                return retv

        if finalbody is None:

            def finalbody(**ctx):
                return retv

        if ctx is None:
            ctx = {}
        retv = None

        try:
            retv = body(**ctx)

        except Exception as exc:
            for h in handlers:
                if type(exc) == h[0]:
                    retv = h[1](exc, **ctx)
                    break

            else:
                raise

        else:
            retv = orelse(**ctx)

        finally:
            retv = finalbody(**ctx)
        return retv

    def x_raise(self, exc, *args, **kwds):
        if callable(exc) and isinstance(exc(), BaseException):
            exc = exc(*args, **kwds)
        if not isinstance(exc, BaseException):
            raise TypeError("exceptions must derive from BaseException")
        raise exc

    def to_dict(self):
        cs = {}

        for name in dir(self):
            if name.startswith("x_"):
                cs[name] = getattr(self, name)
        return cs
