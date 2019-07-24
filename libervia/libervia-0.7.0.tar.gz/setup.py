#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011-2018  Jérôme Poisson (goffi@goffi.org)
# Copyright (C) 2013-2016 Adrien Cossa (souliane@mailoo.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
import os

NAME = "libervia"

install_requires = [
    "sat>=0.7.0",
    "sat-templates",
    "twisted",
    "txJSON-RPC==0.3.1",
    "zope.interface",
    "pyopenssl",
    "jinja2>=2.9",
    "shortuuid",
    "autobahn",
]
long_description = u"""\
Libervia is a web frontend for Salut à Toi (SàT), a multi-frontends and multi-purposes XMPP client.
It features chat, blog, forums, events, tickets, merge requests, file sharing, photo albums, etc.
It is also a decentralized, XMPP based web framework.
"""

with open(os.path.join(NAME, "VERSION")) as v:
    VERSION = v.read().strip()
is_dev_version = VERSION.endswith("D")


def libervia_dev_version():
    """Use mercurial data to compute version"""

    def version_scheme(version):
        return VERSION.replace("D", ".dev0")

    def local_scheme(version):
        return "+{rev}.{distance}".format(rev=version.node[1:], distance=version.distance)

    return {"version_scheme": version_scheme, "local_scheme": local_scheme}


setup(
    name=NAME,
    version=VERSION,
    description=u"Web frontend for Salut à Toi",
    long_description=long_description,
    author="Association « Salut à Toi »",
    author_email="contact@goffi.org",
    url="https://www.salut-a-toi.org",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Twisted",
        "License :: OSI Approved :: GNU Affero General Public License v3 "
        "or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Communications :: Chat",
    ],
    packages=["libervia", "libervia.common", "libervia.server", "twisted.plugins"],
    include_package_data=True,
    data_files=[(os.path.join("share", "doc", NAME), ["COPYING", "README", "INSTALL"])]
    + [
        (os.path.join("share", NAME, root), [os.path.join(root, f) for f in files])
        for root, dirs, files in os.walk(u"themes")
    ],
    scripts=["bin/libervia"],
    zip_safe=False,
    setup_requires=["setuptools_scm"] if is_dev_version else [],
    use_scm_version=libervia_dev_version if is_dev_version else False,
    install_requires=install_requires,
    package_data={"libervia": ["VERSION"]},
    python_requires="~=2.7",
)
