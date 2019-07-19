# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['linux_touchpad']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.0,<4.0', 'pyudev>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'linux-touchpad',
    'version': '0.2.5',
    'description': 'Auto-disable laptop touchpad when a mouse is detected.',
    'long_description': 'A simple, lightweight command line utility for managing your touchpad.\n\n-   Disable when a mouse is detected.\n-   Enabled when no mice are detected.\n-   Toggle this behavior.\n\nFor a more feature-rich implementation, see [touchpad-indicator](https://launchpad.net/touchpad-indicator).\n\n\n# Dependencies\n\n<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">\n\n\n<colgroup>\n<col  class="org-left" />\n\n<col  class="org-left" />\n</colgroup>\n<tbody>\n<tr>\n<td class="org-left">Python 3.7</td>\n<td class="org-left">https://www.python.org/downloads/release/python-373/</td>\n</tr>\n\n\n<tr>\n<td class="org-left">Libinput</td>\n<td class="org-left">https://wiki.archlinux.org/index.php/Libinput</td>\n</tr>\n</tbody>\n</table>\n\n\n# Install\n\n    $ pip install linux-touchpad\n\n\n# Usage\n\n\n## Start\n\nTo begin the process, use this command:\n\n    $ python -m linux_touchpad start\n\n\n## Toggle\n\nEnabled the touchpad and ignore mouse events:\n\n    $ python -m linux_touchpad toggle\n\n\n## Stop\n\n    $ python -m linux_touchpad stop\n\n\n# Author\n\n[Noah Corona](https://github.com/Zer0897)\n[noah@coronasoftware.net](mailto:noah@coronasoftware.net)\n\n[![img](https://coronasoftware.net/s/sLogo.png)](https://coronasoftware.net)\n',
    'author': 'Noah',
    'author_email': 'noah@coronasoftware.net',
    'url': 'https://github.com/Zer0897/linux-touchpad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
