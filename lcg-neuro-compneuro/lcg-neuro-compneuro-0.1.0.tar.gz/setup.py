# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['compneuro', 'compneuro.kernels']

package_data = \
{'': ['*'], 'compneuro.kernels': ['factory/*']}

install_requires = \
['scipy>=1.3,<2.0']

extras_require = \
{'all': ['matplotlib>=3.1,<4.0'], 'matplotlib': ['matplotlib>=3.1,<4.0']}

setup_kwargs = {
    'name': 'lcg-neuro-compneuro',
    'version': '0.1.0',
    'description': 'Computational neuroscience library for Python',
    'long_description': 'lcg-neuro-compneuro – Computational neuroscience library for Python\n===================================================================\n\n|image0|\n|image1|\n\n|image2|\n|image3|\n\n|image4|\n|image5|\n|image6|\n\n-  `Documentation`_\n-  `Issue tracker`_\n-  `Repository contents`_\n-  `History of changes`_\n-  `Contribution/development guide`_\n-  `Copy of MIT License`_\n\n--------------\n\nInstallation\n------------\n\n.. code:: bash\n\n    pip install lcg-neuro-compneuro\n\n--------------\n\n-  Powered by `GitLab CI`_\n-  Created by `Pedro Asad <pasad@lcg.ufrj.br>`_ using `cookiecutter`_ and `gl:pedroasad.com/templates/python/python/app@1.1.0`_\n\n.. _Documentation: https://lcg.gitlab.io/neuro/python-compneuro\n.. _Issue tracker: https://gitlab.com/lcg/neuro/python-compneuro/issues\n.. _Repository contents: MANIFEST.md\n.. _History of changes: CHANGELOG.md\n.. _Contribution/development guide: CONTRIBUTING.md\n.. _Copy of MIT License: LICENSE.txt\n.. _GitLab CI: https://docs.gitlab.com/ee/ci\n.. _Pedro Asad <pasad@lcg.ufrj.br>: mailto:pasad@lcg.ufrj.br\n.. _cookiecutter: http://cookiecutter.readthedocs.io/\n.. _`gl:pedroasad.com/templates/python/python/app@1.1.0`: https://gitlab.com/pedroasad.com/templates/python/python-app/tags/1.1.0\n\n.. |image0| image:: https://img.shields.io/badge/Python-%E2%89%A53.6-blue.svg\n   :target: https://docs.python.org/3.6\n.. |image1| image:: https://img.shields.io/badge/version-0.1.0%20None-orange.svg\n   :target: https://test.pypi.org/project/lcg-neuro-compneuro/0.1.0/\n.. |image2| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://opensource.org/licenses/MIT\n.. |image3| image:: https://img.shields.io/badge/code%20style-Black-black.svg\n   :target: https://pypi.org/project/black/\n.. |image4| image:: https://gitlab.com/lcg/neuro/python-compneuro/badges/master/pipeline.svg\n   :target: https://gitlab.com/lcg/neuro/python-compneuro\n.. |image5| image:: https://img.shields.io/badge/security-Check%20here!-yellow.svg\n   :target: https://gitlab.com/lcg/neuro/python-compneuro/security\n.. |image6| image:: https://codecov.io/gl/lcg:neuro/python-compneuro/branch/master/graph/badge.svg\n   :target: https://codecov.io/gl/lcg:neuro/python-compneuro\n',
    'author': 'Pedro Asad',
    'author_email': 'pasad@lcg.ufrj.br',
    'url': 'https://lcg.gitlab.io/neuro/python-compneuro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
