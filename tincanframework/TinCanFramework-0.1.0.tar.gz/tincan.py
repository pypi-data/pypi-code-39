#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# As with Bottle, it's all in one big, ugly file. For now.

# I m p o r t s

import os, sys
import ast
import binascii
from base64 import b16encode, b16decode
from chameleon import PageTemplate, PageTemplateFile, TemplateError
import email.utils
import functools
import importlib
from inspect import isclass
import io
import logging
import mimetypes
import py_compile
from stat import S_ISDIR, S_ISREG
from string import whitespace
from threading import Lock
import time
import urllib

import bottle

# E x c e p t i o n s

class TinCanException(Exception):
    """
    The parent class of all exceptions we raise.
    """
    pass

class TemplateHeaderError(TinCanException):
    """
    Raised upon encountering a syntax error in the template headers.
    """
    def __init__(self, message, line):
        super().__init__(message, line)
        self.message = message
        self.line = line

    def __str__(self):
        return "line {0}: {1}".format(self.line, self.message)

class LoadError(TinCanException):
    """
    Raised when we run into problems #load'ing something, usually
    because it doesn't exist.
    """
    def __init__(self, message, source):
        super().__init__(message, source)
        self.message = message
        self.source = source

    def __str__(self):
        return "{0}: #load error: {1}".format(self.source, self.message)

class ForwardException(TinCanException):
    """
    Raised to effect the flow control needed to do a forward (server-side
    redirect). It is ugly to do this, but other Python frameworks do and
    there seems to be no good alternative.
    """
    def __init__(self, target):
        self.target = target

class TinCanError(TinCanException):
    """
    General-purpose exception thrown by TinCan when things go wrong, often
    when attempting to launch webapps.
    """
    pass

# T e m p l a t e s
#
# Template (.pspx) files. These are standard templates for a supported
# template engine, but with an optional set of header lines that begin
# with '#'.

class TemplateFile(object):
    """
    Parse a template file into a header part and the body part. The header
    is always a leading set of lines, each starting with '#', that is of the
    same format regardless of the template body. The template body varies
    depending on the selected templating engine. The body part has
    each header line replaced by a blank line. This preserves the overall
    line numbering when processing the body. The added newlines are normally
    stripped out before the rendered page is sent back to the client.
    """
    _END = "#end"
    _LEND = len(_END)
    _WS = set(whitespace)

    def __init__(self, raw, encoding='utf-8'):
        if isinstance(raw, io.TextIOBase):
            self._do_init(raw)
        elif isinstance(raw, str):
            with open(raw, "r", encoding=encoding) as fp:
                self._do_init(fp)
        else:
            raise TypeError("Expecting a string or Text I/O object.")

    def _do_init(self, fp):
        self._hbuf = []
        self._bbuf = []
        self._state = self._header
        while True:
            line = fp.readline()
            if line == '':
                break
            self._state(line)
        self.header = ''.join(self._hbuf)
        self.body = ''.join(self._bbuf)

    def _header(self, line):
        if not line.startswith('#'):
            self._state = self._body
            self._state(line)
            return
        if line.startswith(self._END) and (len(line) == self._LEND or line[self._LEND] in self._WS):
            self._state = self._body
        self._hbuf.append(line)
        self._bbuf.append("\n")

    def _body(self, line):
        self._bbuf.append(line)

class TemplateHeader(object):
    """
    Parses and represents a set of header lines.
    """
    _NAMES = [ "errors", "forward", "methods", "python", "template" ]
    _FNAMES = [ "hidden" ]
    _ANAMES = [ "load" ]

    def __init__(self, string):
        # Initialize our state
        for i in self._NAMES:
            setattr(self, i, None)
        for i in self._FNAMES:
            setattr(self, i, False)
        for i in self._ANAMES:
            setattr(self, i, [])
        # Parse the string
        count = 0
        nameset = set(self._NAMES + self._FNAMES + self._ANAMES)
        seen = set()
        lines = string.split("\n")
        if lines and lines[-1] == "":
            del lines[-1]
        for line in lines:
            # Get line
            count += 1
            if not line.startswith("#"):
                raise TemplateHeaderError("Does not start with '#'.", count)
            try:
                rna, rpa = line.split(maxsplit=1)
            except ValueError:
                rna = line.rstrip()
                rpa = None
            # Get name, ignoring remarks.
            name = rna[1:]
            if name == "rem":
                continue
            if name == "end":
                break
            if name not in nameset:
                raise TemplateHeaderError("Invalid directive: {0!r}".format(rna), count)
            if name in seen:
                raise TemplateHeaderError("Duplicate {0!r} directive.".format(rna), count)
            if name not in self._ANAMES:
                seen.add(name)
            # Flags
            if name in self._FNAMES:
                setattr(self, name, True)
                continue
            # Get parameter
            if rpa is None:
                raise TemplateHeaderError("Missing parameter.", count)
            param = rpa.strip()
            for i in [ "'", '"']:
                if param.startswith(i) and param.endswith(i):
                    param = ast.literal_eval(param)
                    break
            # Update this object
            if name in self._ANAMES:
                getattr(self, name).append(param)
            else:
                setattr(self, name, param)

# C h a m e l e o n
#
# Support for Chameleon templates (the kind TinCan uses).

class ChameleonTemplate(bottle.BaseTemplate):
    def prepare(self, **options):
        if self.source:
            self.tpl = PageTemplate(self.source, **options)
        else:
            self.tpl = PageTemplateFile(self.filename, encoding=self.encoding,
                search_path=self.lookup, **options)
            # XXX - work around broken Chameleon decoding
            self.tpl.default_encoding = self.encoding

    def render(self, *args, **kwargs):
        for dictarg in args:
            kwargs.update(dictarg)
        _defaults = self.defaults.copy()
        _defaults.update(kwargs)
        return self.tpl.render(**_defaults)

chameleon_template = functools.partial(bottle.template, template_adapter=ChameleonTemplate)
chameleon_view = functools.partial(bottle.view, template_adapter=ChameleonTemplate)

# U t i l i t i e s

def _normpath(base, unsplit):
    """
    Split, normalize and ensure a possibly relative path is absolute. First
    argument is a list of directory names, defining a base. Second
    argument is a string, which may either be relative to that base, or
    absolute. Only '/' is supported as a separator.
    """
    scratch = unsplit.strip('/').split('/')
    if not unsplit.startswith('/'):
        scratch = base + scratch
    ret = []
    for i in scratch:
        if i == '.':
            continue
        if i == '..':
            ret.pop()  # may raise IndexError
            continue
        ret.append(i)
    return ret

def _mangle(string):
    """
    Turn a possibly troublesome identifier into a mangled one.
    """
    first = True
    ret = []
    for ch in string:
        if ch == '_' or not (ch if first else "x" + ch).isidentifier():
            ret.append('_')
            ret.append(b16encode(ch.encode("utf-8")).decode("us-ascii"))
        else:
            ret.append(ch)
        first = False
    return ''.join(ret)

_FOLDS_CASE = sys.platform in ['darwin', 'win32']

def _casef(string, case="lower"):
    """
    If we're on an OS with case-insensitive file names, fold case.
    Else leave things alone.
    """
    return getattr(string, case)() if _FOLDS_CASE else string

# The TinCan class. Simply a Bottle webapp that contains a forward method, so
# the code-behind can call request.app.forward().

class TinCan(bottle.Bottle):
    def forward(self, target):
        """
        Forward this request to the specified target route.
        """
        source = bottle.request.environ['PATH_INFO']
        base = source.strip('/').split('/')[:-1]
        if bottle.request.environ.get(_FTYPE, False):
            raise TinCanError("{0}: forward from error page".format(source))
        try:
            exc = ForwardException('/' + '/'.join(_normpath(base, target)))
        except IndexError as e:
            raise TinCanError("{0}: invalid forward to {1!r}".format(source, target)) from e
        raise exc

# C o d e   B e h i n d
#
# Represents the code-behind of one of our pages. This gets subclassed, of
# course.

class BasePage(object):
    """
    The parent class of both error and normal pages' code-behind.
    """
    def handle(self):
        """
        This is the entry point for the code-behind logic. It is intended
        to be overridden.
        """
        pass

    def export(self):
        """
        Export template variables. The default behavior is to export all
        non-hidden non-callables that don't start with an underscore.
        This method can be overridden if a different behavior is
        desired. It should always return a dict or dict-like object.
        """
        ret = { 'page': self }
        for name in dir(self):
            if name in self._HIDDEN or name.startswith('_'):
                continue
            value = getattr(self, name)
            if callable(value):
                continue
            ret[name] = value
        return ret

class Page(BasePage):
    """
    The code-behind for a normal page.
    """
    # Non-private things we refuse to export anyhow.
    _HIDDEN = set([ "request", "response" ])

    def __init__(self, req, resp):
        """
        Constructor. This is a lightweight operation.
        """
        self.request = req  # app context is request.app in Bottle
        self.response = resp

class ErrorPage(BasePage):
    """
    The code-behind for an error page.
    """
    _HIDDEN = set()

    def __init__(self, req, err):
        """
        Constructor. This is a lightweight operation.
        """
        self.request = req
        self.error = err

# I n c l u s i o n
#
# Most processing is in the TinCanRoute class; this just interprets and
# represents arguments to the #load header directive.

class _LoadedFile(object):
    def __init__(self, raw):
        if raw.startswith('<') and raw.endswith('>'):
            raw = raw[1:-1]
            self.in_lib = True
        else:
            self.in_lib = False
        equals = raw.find('=')
        if equals < 0:
            self.vname = os.path.splitext(os.path.basename(raw))[0]
            self.fname = raw
        else:
            self.vname = raw[:equals]
            self.fname = raw[equals+1:]
        if self.vname == "":
            raise ValueError("empty variable name")
        if self.fname == "":
            raise ValueError("empty file name")
        if not _casef(self.fname).endswith(_IEXTEN):
            raise ValueError("file does not end in {0}".format(_IEXTEN))

# Using a cache is likely to help efficiency a lot, since many pages
# will typically #load the same standard stuff. Except if we're
# multithreading, then we want each page's templates to be private.
_tcache = {}
def _get_template_cache(name, direct, coding):
    aname = os.path.abspath(os.path.join(direct, name))
    if aname not in _tcache:
        tmpl = ChameleonTemplate(name=name, lookup=[direct], encoding=coding)
        assert aname == tmpl.filename
        _tcache[aname] = tmpl
    return _tcache[aname]

def _get_template_nocache(name, direct, coding):
    return ChameleonTemplate(name=name, lookup=[direct], encoding=coding)

# R o u t e s
#
# Represents a route in TinCan. Our launcher creates these on-the-fly based
# on the files it finds.

_ERRMIN = 400
_ERRMAX = 599
_IEXTEN = ".pt"
_PEXTEN = ".py"
_TEXTEN = ".pspx"
_FLOOP = "tincan.forwards"
_FORIG = "tincan.origin"
_FTYPE = "tincan.iserror"
_INDEX = "/index" + _TEXTEN
_LINDEX = len(_INDEX)
_INDICES = [ _INDEX, "/index.html", "/index.htm" ]

class _TinCanBaseRoute(object):
    """
    The base class for all NON ERROR routes. Error routes are just a little
    bit different.
    """
    def __init__(self, launcher, name, subdir):
        global _get_template_cache, _get_template_nocache
        if launcher.multithread:
            self.lock = Lock()
            self.get_template = _get_template_nocache
        else:
            self.lock = _DummyLock()
            self.get_template = _get_template_cache
        self.logger = launcher.logger

    def urljoin(self, *args):
        """
        Normalize a parsed-out URL fragment.
        """
        args = list(args)
        if args[0] == '/':
            args[0] = ''
        return '/'.join(args)

    def launch(self):
        raise NotImplementedError("This must be overridden.")

    def __call__(self):
        raise NotImplementedError("This must be overridden.")

class _TinCanStaticRoute(_TinCanBaseRoute):
    """
    A route to a static file. These are useful for test servers. For
    production servers, one is better off using a real web server and
    a WSGI plugin, and having that handle static files. Much of this
    logic is cribbed from the Bottle source code (we don't call it
    directly because it is undocumented and thus subject to change).
    """
    def __init__(self, launcher, name, subdir):
        super().__init__(launcher, name, subdir)
        self._app = launcher.app
        self._fspath = os.path.join(launcher.fsroot, *subdir, name)
        self._urlpath = self.urljoin(launcher.urlroot, *subdir, name)
        self._type = mimetypes.guess_type(name)[0]
        if self._type is None:
            self._type = "application/octet-stream"
        if self._type.startswith("text/"):
            self._encoding = launcher.encoding
            self._type += "; charset=" + launcher.encoding
        else:
            self._encoding = None

    def launch(self):
        self.logger.info("adding static route: %s", self._urlpath)
        self._app.route(self._urlpath, 'GET', self)
        for i in _INDICES:
            if _casef(self._urlpath).endswith(i):
                li = len(i)
                for j in [ self._urlpath[:1-li], self._urlpath[:-li] ]:
                    if j:
                        self.logger.info("adding static route: %s", j)
                        self._app.route(j, 'GET', self)

    def _parse_date(self, ims):
        """
        Parse rfc1123, rfc850 and asctime timestamps and return UTC epoch.
        """
        try:
            ts = email.utils.parsedate_tz(ims)
            return time.mktime(ts[:8] + (0,)) - (ts[9] or 0) - time.timezone
        except (TypeError, ValueError, IndexError, OverflowError):
            return None

    def __call__(self):
        # Get file contents and time stamp. If we can't, return an
        # appropriate HTTP error response.
        try:
            with open(self._fspath, "rb") as fp:
                mtime = os.fstat(fp.fileno()).st_mtime
                bytes = fp.read()
        except FileNotFoundError as e:
            return bottle.HTTPError(status=404, exception=e)
        except PermissionError as e:
            return bottle.HTTPError(status=403, exception=e)
        except OSError as e:
            self.logger.exception("unexpected exception reading %r", self._fspath)
            return bottle.HTTPError(status=500, exception=e)
        # Establish preliminary standard headers.
        headers = {
            "Content-Type": self._type,
            "Last-Modified": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(mtime)),
        }
        if self._encoding:
            headers["Content-Encoding"] = self._encoding
        # Support the If-Modified-Since request header.
        ims = bottle.request.environ.get('HTTP_IF_MODIFIED_SINCE')
        if ims:
            ims = self._parse_date(ims.split(";")[0].strip())
        if ims is not None and ims >= int(mtime):
            headers["Content-Length"] = "0"
            return bottle.HTTPResponse(body=b"", status=304, headers=headers)
        # Standard response.
        headers["Content-Length"] = str(len(bytes))
        return bottle.HTTPResponse(body=bytes, status=200, headers=headers)

class _TinCanErrorRoute(object):
    """
    A route to an error page. These don't get routes created for them,
    and are only reached if an error routes them there. Unless you create
    custom code-behind, only two variables are available to your template:
    request (bottle.Request) and error (bottle.HTTPError).
    """
    def __init__(self, template, loads, klass, lock, logger):
        self._template = template
        self._template.prepare()
        self._loads = loads
        self._class = klass
        self.lock = lock
        self.logger = logger

    def __call__(self, e):
        bottle.request.environ[_FTYPE] = True
        try:
            obj = self._class(bottle.request, e)
            obj.handle()
            tvars = self._loads.copy()
            tvars.update(obj.export())
            with self.lock:
                return self._template.render(tvars).lstrip('\n')
        except bottle.HTTPResponse as e:
            return e
        except Exception as e:
            self.logger.exception("unexpected exception in error page")
            # Bottle doesn't allow error handlers to themselves cause
            # errors, most likely as a measure to prevent looping. So
            # this will cause a "Critical error while processing request"
            # page to be displayed, and any installed error pages to be
            # ignored.
            raise bottle.HTTPError(status=500, exception=e)

class _TinCanRoute(_TinCanBaseRoute):
    """
    A route created by the TinCan launcher.
    """
    def __init__(self, launcher, name, subdir):
        super().__init__(launcher, name, subdir)
        self._fsroot = launcher.fsroot
        self._urlroot = launcher.urlroot
        self._name = name
        self._python = name + _PEXTEN
        self._fspath = os.path.join(launcher.fsroot, *subdir, name + _TEXTEN)
        self._urlpath = self.urljoin(launcher.urlroot, *subdir, name + _TEXTEN)
        self._origin = self._urlpath
        self._subdir = subdir
        self._seen = set()
        self._app = launcher.app
        self._encoding = launcher.encoding

    def launch(self):
        """
        Launch a single page.
        """
        # Build master and header objects, process #forward directives
        oheader = None
        while True:
            try:
                self._template = TemplateFile(self._fspath)
            except IOError as e:
                if oheader is not None:
                    note = "{0}: invalid #forward: ".format(self._origin)
                else:
                    note = ""
                raise TinCanError("{0}{1!s}".format(note, e)) from e
            try:
                self._header = TemplateHeader(self._template.header)
            except TemplateHeaderError as e:
                raise TinCanError("{0}: {1!s}".format(self._fspath, e)) from e
            if oheader is None:
                oheader = self._header  # save original header
            elif (oheader.errors is None) != (self._header.errors is None):
                raise TinCanError("{0}: invalid #forward".format(self._origin))
            if self._header.forward is None:
                break
            # self.logger.debug("forwarding from: %s", self._urlpath)  # debug
            self._redirect()
            # self.logger.debug("forwarded to: %s", self._urlpath)  # debug
        # If this is a #hidden page, we ignore it for now, since hidden pages
        # don't get routes made for them.
        if oheader.hidden and not oheader.errors:
            return
        # Get the code-behind #python
        if self._header.python is None:
            self._python_specified = False
        else:
            if not _casef(self._header.python).endswith(_PEXTEN):
                raise TinCanError("{0}: #python files must end in {1}".format(self._urlpath, _PEXTEN))
            self._python = self._header.python
            self._python_specified = True
        # Obtain a class object by importing and introspecting a module.
        self._getclass()
        # Build body object (#template) and obtain #loads.
        if self._header.template is not None:
            if not _casef(self._header.template).endswith(_TEXTEN):
                raise TinCanError("{0}: #template files must end in {1}".format(self._urlpath, _TEXTEN))
            try:
                rtpath = self._splitpath(self._header.template)
                tpath = os.path.normpath(os.path.join(self._fsroot, *rtpath))
                tfile = TemplateFile(tpath)
            except OSError as e:
                raise TinCanError("{0}: invalid #template: {1!s}".format(self._urlpath, e)) from e
            except IndexError as e:
                raise TinCanError("{0}: invalid #template".format(self._urlpath)) from e
            self._body = self._mktemplate(tfile.body, self.urljoin(*rtpath))
        else:
            self._body = self._mktemplate(self._template.body, self._urlpath)
        self._body.prepare()
        # Process loads
        self._loads = {}
        for load in self._header.load:
            try:
                load = _LoadedFile(load)
            except ValueError as e:
                raise TinCanError("{0}: bad #load: {1!s}".format(self._urlpath, e)) from e
            if load.in_lib:
                fdir = os.path.join(self._fsroot, _WINF, "tlib")
            else:
                fdir = os.path.join(self._fsroot, *self._subdir)
            try:
                tmpl = self.get_template(load.fname, fdir, self._encoding)
            except Exception as e:
                raise TinCanError("{0}: bad #load: {1!s}".format(self._urlpath, e)) from e
            self._loads[load.vname] = tmpl.tpl
        # If this is an #errors page, register it as such.
        if oheader.errors is not None:
            self._mkerror(oheader.errors)
            return  # this implies #hidden
        # Get #methods for this route
        if self._header.methods is None:
            methods = [ 'GET' ]
        else:
            methods = [ i.upper() for i in self._header.methods.split() ]
            if not methods:
                raise TinCanError("{0}: no #methods specified".format(self._urlpath))
        # Register this thing with Bottle
        mtxt = ','.join(methods)
        self.logger.info("adding route: %s (%s)", self._origin, mtxt)
        self._app.route(self._origin, methods, self)
        if _casef(self._origin).endswith(_INDEX):
            for i in [ self._origin[:1-_LINDEX], self._origin[:-_LINDEX] ]:
                if i:
                    self.logger.info("adding route: %s (%s)", i, mtxt)
                    self._app.route(i, methods, self)

    def _mktemplate(self, source, name):
        try:
            return ChameleonTemplate(source=source, encoding=self._encoding)
        except TemplateError as e:
            raise TinCanError("{0}: {1!s}".format(name, e)) from e

    def _splitpath(self, unsplit):
        return _normpath(self._subdir, unsplit)

    def _mkerror(self, rerrors):
        try:
            errors = [ int(i) for i in rerrors.split() ]
        except ValueError as e:
            raise TinCanError("{0}: bad #errors line".format(self._urlpath)) from e
        if not errors:
            errors = range(_ERRMIN, _ERRMAX+1)
        route = _TinCanErrorRoute(
            ChameleonTemplate(source=self._template.body, encoding=self._encoding),
            self._loads, self._class, self.lock, self.logger)
        for error in errors:
            if error < _ERRMIN or error > _ERRMAX:
                raise TinCanError("{0}: bad #errors code".format(self._urlpath))
            self._app.error_handler[error] = route  # XXX

    def _gettime(self, path):
        try:
            return os.stat(path).st_mtime
        except FileNotFoundError:
            return 0
        except OSError as e:
            raise TinCanError(str(e)) from e

    def _getclass(self):
        try:
            pypath = os.path.normpath(os.path.join(self._fsroot, *self._splitpath(self._python)))
        except IndexError as e:
            raise TinCanError("{0}: invalid #python".format(self._urlpath)) from e
        klass = ErrorPage if self._header.errors else Page
        # Give 'em a default code-behind if they don't furnish one
        pytime = self._gettime(pypath)
        if not pytime:
            if self._python_specified:
                raise TinCanError("{0}: #python file not found".format(self._urlpath))
            self._class = klass
            return
        # Else load the code-behind from a .py file
        pycpath = pypath + 'c'
        pyctime = self._gettime(pycpath)
        try:
            if pyctime < pytime:
                py_compile.compile(pypath, cfile=pycpath, doraise=True)
        except py_compile.PyCompileError as e:
            raise TinCanError(str(e)) from e
        except Exception as e:
            raise TinCanError("{0}: {1!s}".format(pypath, e)) from e
        try:
            spec = importlib.util.spec_from_file_location(_mangle(self._name), pycpath)
            mod =  importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception as e:
            raise TinCanError("{0}: error importing: {1!s}".format(pycpath, e)) from e
        # Locate a suitable class. We look for the "deepest" class object
        # we can find in the inheritance tree.
        self._class = None
        score = -1
        ambig = False
        for i in dir(mod):
            v = getattr(mod, i)
            if not isclass(v):
                continue
            d = self._cldepth(klass, v)
            if d > score:
                self._class = v
                score = d
                ambig = False
            elif d == score:
                ambig = True
        if self._class is None:
            raise TinCanError("{0}: contains no {1} classes".format(pypath, klass.__name__))
        if ambig:
            raise TinCanError("{0}: contains ambiguous {1} classes".format(pypath, klass.__name__))

    # This might fail for complex inheritance schemes from the classes of
    # interest (so don't use them!).
    def _cldepth(self, base, klass, count=0):
        if klass is object:
            # not found
            return -1
        elif klass is base:
            # just found
            return count
        else:
            # must recurse
            for c in klass.__bases__:
                result = self._cldepth(base, c, count=count+1)
                if result > 0:
                    return result
            return -1

    def _redirect(self):
        try:
            rlist = self._splitpath(self._header.forward)
            forw = '/' + '/'.join(rlist)
            if forw in self._seen:
                raise TinCanError("{0}: #forward loop".format(self._origin))
            self._seen.add(forw)
            rname = rlist.pop()
        except IndexError as e:
            raise TinCanError("{0}: invalid #forward".format(self._urlpath)) from e
        name, ext = os.path.splitext(rname)
        if _casef(ext) != _TEXTEN:
            raise TinCanError("{0}: invalid #forward".format(self._urlpath))
        self._subdir = rlist
        self._python = name + _PEXTEN
        self._fspath = os.path.join(self._fsroot, *self._subdir, rname)
        self._urlpath = '/' + self.urljoin(*self._subdir, rname)

    def __call__(self):
        """
        This gets called by the framework AFTER the page is launched.
        """
        target = None
        try:
            obj = self._class(bottle.request, bottle.response)
            obj.handle()
            tvars = self._loads.copy()
            tvars.update(obj.export())
            with self.lock:
                return self._body.render(tvars).lstrip('\n')
        except ForwardException as fwd:
            target = fwd.target
        except bottle.HTTPResponse as e:
            return e
        except Exception as e:
            self.logger.exception("%s: unexpected exception", self._urlpath)
            raise bottle.HTTPError(status=500, exception=e)
        if target is None:
            self.logger.error("%s: unexpected null target", self._urlpath)
            raise bottle.HTTPError(status=500, exception=TinCanError(message))
        # We get here if we are doing a server-side programmatic
        # forward.
        environ = bottle.request.environ
        if _FORIG not in environ:
            environ[_FORIG] = self._urlpath
        if _FLOOP not in environ:
            environ[_FLOOP] = set([self._urlpath])
        elif target in environ[_FLOOP]:
            self.logger.error("%s: forward loop detected", environ[_FORIG])
            raise bottle.HTTPError(status=500, exception=TinCanError(message))
        environ[_FLOOP].add(target)
        environ['bottle.raw_path'] = target
        environ['PATH_INFO'] = urllib.parse.quote(target)
        route, args = self._app.router.match(environ)
        environ['route.handle'] = environ['bottle.route'] = route
        environ['route.url_args'] = args
        return route.call(**args)

# M u t e x
#
# A dummy lock class, which is what we use if we don't need locking.

class _DummyLock(object):
    def acquire(self, blocking=True, timeout=-1):
        pass

    def release(self):
        pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return False

# L a u n c h e r

_WINF = "WEB-INF"
_EBANNED = set([_IEXTEN, _TEXTEN, _PEXTEN, _PEXTEN+"c"])
ENCODING = "utf-8"
_BITBUCKET = logging.getLogger(__name__)
_BITBUCKET.addHandler(logging.NullHandler)

class _Launcher(object):
    """
    Helper class for launching webapps.
    """
    def __init__(self, fsroot, urlroot, multithread):
        """
        Lightweight constructor. The real action happens in .launch() below.
        """
        self.fsroot = fsroot
        self.urlroot = urlroot
        self.app = None
        self.errors = 0
        self.debug = False
        self.encoding = ENCODING
        self.static = False
        self.multithread = multithread
        self.logger = _BITBUCKET

    def launch(self):
        """
        Does the actual work of launching something. XXX - modifies sys.path
        and never un-modifies it.
        """
        # Sanity checks
        if not self.urlroot.startswith("/"):
            self.errors = 1
            self.logger("urlroot not absolute: {0!r}".format(self.urlroot))
            return self
        if not os.path.isdir(self.fsroot):
            self.errors = 1
            self.logger("no such directory: {0!r}".format(self.fsroot))
            return self
        # Make any needed directories. Refuse to launch things that don't
        # contain WEB-INF, to prevent accidental launches of undesired
        # directory trees containing sensitive files.
        winf = os.path.join(self.fsroot, _WINF)
        if not os.path.isdir(winf):
            self.errors = 1
            self.logger("no WEB-INF directory in {0!r}".format(self.fsroot))
            return self
        lib = os.path.join(winf, "lib")
        for i in [ lib ]:
            if not os.path.isdir(i):
                os.mkdir(i)
        # Add our private lib directory to sys.path
        sys.path.insert(1, os.path.abspath(lib))
        # Do what we gotta do
        self.app = TinCan()
        config = self.app.config
        config['tincan.fsroot'] = os.path.abspath(self.fsroot)
        config['tincan.urlroot'] = self.urlroot
        config['tincan.logger'] = self.logger
        config['tincan.encoding'] = self.encoding
        self._launch([])
        return self

    def _launch(self, subdir):
        for entry in os.listdir(os.path.join(self.fsroot, *subdir)):
            if entry.startswith("."):
                continue  # hidden file
            if not subdir and _casef(entry, "upper") == _WINF:
                continue
            etype = os.stat(os.path.join(self.fsroot, *subdir, entry)).st_mode
            if S_ISREG(etype):
                ename, eext = os.path.splitext(entry)
                eext = _casef(eext)
                if eext == _TEXTEN:
                    route = _TinCanRoute(self, ename, subdir)
                else:
                    if eext in _EBANNED:
                        continue
                    if self.static:
                        route = _TinCanStaticRoute(self, entry, subdir)
                    else:
                        continue
                try:
                    route.launch()
                except TinCanError as e:
                    if self.logger.getEffectiveLevel() <= logging.DEBUG:
                        self.logger.exception(str(e))
                    else:
                        self.logger.error(str(e))
                    self.errors += 1
            elif S_ISDIR(etype):
                self._launch(subdir + [entry])

def launch(fsroot=None, urlroot='/', multithread=True, **kwargs):
    """
    Launch and return a TinCan webapp. Does not run the app; it is the
    caller's responsibility to call app.run()
    """
    if fsroot is None:
        fsroot = os.getcwd()
    launcher = _Launcher(fsroot, urlroot, multithread)
    allowed = set(["logger", "encoding", "static"])
    for k, v in kwargs.items():
        if k not in allowed:
            raise TypeError("launch() got an unexpected keyword argument {0!r}".format(k))
        setattr(launcher, k, v)
    launcher.launch()
    return launcher.app, launcher.errors

# XXX - We cannot implement a command-line launcher here; see the
# launcher script for why.
