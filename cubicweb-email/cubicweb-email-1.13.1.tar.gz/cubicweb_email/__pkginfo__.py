# pylint: disable=W0622
"""cubicweb-email packaging information"""

modname = 'email'
distname = "cubicweb-%s" % modname

numversion = (1, 13, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname
description = "email component for the CubicWeb framework"
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
__depends__ = {
    'cubicweb': '>= 3.24',
    'cubicweb-file': '>= 1.9.0',
    'cwclientlib': '>= 0.3.1',
}
