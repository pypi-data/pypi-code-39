# -*- coding: utf-8 -*-
"""
Programatic interface to package structure.
"""
# pylint: disable=too-many-instance-attributes,too-many-locals,R0903
from __future__ import print_function
try:
    import ConfigParser as configparser
    from cStringIO import StringIO
except ImportError:  # pragma: nocover
    import configparser
    from io import StringIO

from dkfileutils.path import Path


class DefaultPackage(object):
    """Default package directory layout (consider this abstract, both in the
       sense that this class is abstract and in the sense that this is the
       attribute names of this object, not neccessarily the actual directory
       name)

      ::

          <parent>                      # self.location (abspath)
             |--<name>                  # self.root (abspath), self.package_name
                  |-- build             # self.build
                  |   |-- coverage      # self.build_coverage
                  |   |-- docs          # self.build_docs
                  |   |-- lintscore     # self.build_lintscore
                  |   |-- meta          # self.build_meta
                  |   `-- pytest        # self.build_pytest
                  |-- <name>            # <name> == self.name, self.source
                  |   |-- js            # self.source_js
                  |   |-- less          # self.source_less
                  |   |-- static        # self.django_static
                  |   `-- templates     # self.django_templates
                  |-- docs              # self.docs
                  +-- tests             # self.tests
                  +-- setup.py          #
                  `-- requirements.txt  #

    """
    #: A set of all overridable keys
    KEYS = {
        'location',
        'package_name',
        'name',
        'docs',
        'tests',
        'tests_js',
        'build',
        'source',
        'source_js',
        'source_less',
        'django_templates',
        'django_static',
        'build_coverage',
        'build_docs',
        'build_lintscore',
        'build_meta',
        'build_pytest',
    }

    def __init__(self, root, **kw):
        #: The abspath to the "working copy".
        self.root = kw.get('root', Path(root).abspath())
        #: The abspath of the directory containing the root.
        self.location = kw.get('location', self.root.parent)     # pylint: disable=no-member
        #: The pip-installable name.
        self.package_name = kw.get('package_name', self.root.basename())
        #: The importable name.
        self.name = kw.get('name', self.package_name.replace('-', ''))
        #: The documentation source directory.
        self.docs = kw.get('docs', self.root / 'docs')
        #: The tests directory.
        self.tests = kw.get('tests', self.root / 'tests')
        #: the javascript tests directory
        self.tests_js = kw.get('tests_js', self.root / 'tests' / 'js')
        #: The root of the build output directory.
        self.build = kw.get('build', self.root / 'build')
        #: The source directory.
        self.source = kw.get('source', self.root / self.name)

        #: The javascript source directory.
        self.source_js = kw.get('source_js', self.root / self.name / 'js')
        #: The less source directory.
        self.source_less = kw.get('source_less', self.root / self.name / 'less')
        #: The django app template directory.
        self.django_templates = kw.get('django_templates', self.root / self.name / 'templates')
        #: The django app static directory.
        self.django_static = kw.get('django_static', self.root / self.name / 'static')

        #: Coverage output directory.
        self.build_coverage = kw.get('build_coverage', self.root / 'build' / 'coverage')
        #: Documentation output directory.
        self.build_docs = kw.get('build_docs', self.root / 'build' / 'docs')
        #: Lintscore output directory.
        self.build_lintscore = kw.get('build_lintscore', self.root / 'build' / 'lintscore')
        #: Package meta output directory.
        self.build_meta = kw.get('build_meta', self.root / 'build' / 'meta')
        #: Pytest output directory.
        self.build_pytest = kw.get('build_pytest', self.root / 'build' / 'pytest')

        for k, v in kw.items():
            setattr(self, k, v)

    def is_django(self):
        return any(d.exists() for d in self.django_dirs)

    @property
    def source_dirs(self):
        """Directories containing source.
        """
        return [self.source, self.source_js, self.source_less]

    @property
    def django_dirs(self):
        """Directories containing/holding django specific files.
        """
        return [self.django_static, self.django_templates]

    @property
    def build_dirs(self):
        """Directories containing build artifacts.
        """
        return [self.build, self.build_coverage, self.build_docs,
                self.build_lintscore, self.build_meta, self.build_pytest]

    @property
    def all_dirs(self):
        """Return all package directories.
        """
        return ([self.docs, self.tests]
                + self.source_dirs
                + self.django_dirs
                + self.build_dirs)

    def missing_dirs(self):
        """Return all missing directories.
        """
        return [d for d in self.all_dirs if not d.exists()]

    def make_missing(self):
        """Create all missing directories.
        """
        for d in self.missing_dirs():
            d.makedirs()

    def __repr__(self):
        keylen = max(len(k) for k in self.__dict__.keys())
        # vallen = max(len(k) for k in self.__dict__.values())
        lines = []
        for k, v in sorted(self.__dict__.items()):
            lines.append("%*s %-s" % (keylen, k, v))
        return '\n'.join(lines)

    def write_ini(self, fname, section):
        """Write to ini file.
        """
        cp = configparser.RawConfigParser()
        cp.add_section(section)
        vals = [
            'root', 'location', 'name', 'docs', 'tests', 'source', 'source_js',
            'source_less', 'build', 'build_coverage', 'build_docs',
            'build_lintscore', 'build_meta', 'build_pytest',
            'django_templates', 'django_static',
        ]
        for val in vals:
            cp.set(section, val, getattr(self, val))

        out = StringIO()
        cp.write(out)
        return out.getvalue()


class Package(DefaultPackage):
    """Package layout with possible overrides.
    """
    
    def __init__(self, root,
                 # name=None,
                 # docs=None,
                 # tests=None,
                 # build=None,
                 # source=None,
                 # source_js=None,
                 # source_less=None,
                 # build_coverage=None,
                 # build_docs=None,
                 # build_lintscore=None,
                 # build_meta=None,
                 # build_pytest=None,
                 # django_templates=None,
                 # django_static=None,
                 **kw):
        # pylint: disable=multiple-statements,too-many-arguments,R0912
        super(Package, self).__init__(root, **kw)

        name = kw.get('name')
        docs = kw.get('docs')
        tests = kw.get('tests')
        build = kw.get('build')
        source = kw.get('source')
        source_js = kw.get('source_js')
        source_less = kw.get('source_less')
        build_coverage = kw.get('build_coverage')
        build_docs = kw.get('build_docs')
        build_lintscore = kw.get('build_lintscore')
        build_meta = kw.get('build_meta')
        build_pytest = kw.get('build_pytest')
        django_templates = kw.get('django_templates')
        django_static = kw.get('django_static')

        if name: self.name = name
        if docs: self.docs = docs
        if tests: self.tests = tests
        if build:
            self.build = build
            self.build_coverage = self.build / 'coverage'
            self.build_docs = self.build / 'docs'
            self.build_lintscore = self.build / 'lintscore'
            self.build_meta = self.build / 'meta'
            self.build_pytest = self.build / 'pytest'
        if source:
            self.source = source
            self.source_js = self.source / 'js'
            self.source_less = self.source / 'less'
            self.django_templates = self.source / 'templates'
            self.django_static = self.source / 'static'
        if source_js: self.source_js = source_js
        if source_less: self.source_less = source_less
        if build_coverage: self.build_coverage = build_coverage
        if build_docs: self.build_docs = build_docs
        if build_lintscore: self.build_lintscore = build_lintscore
        if build_meta: self.build_meta = build_meta
        if build_pytest: self.build_pytest = build_pytest
        if django_templates: self.django_templates = django_templates
        if django_static: self.django_static = django_static
