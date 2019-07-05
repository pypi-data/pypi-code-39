# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_tps']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0']

setup_kwargs = {
    'name': 'py-tps',
    'version': '0.1.7',
    'description': 'This is a simple library for reading and writing .tps files as created and used by the tpsDig landmarking tool created by F. James Rohlf.  https://life.bio.sunysb.edu/morph/',
    'long_description': 'This is a simple library for reading and writing .tps files as created and used by the tpsDig landmarking tool\ncreated by F. James Rohlf.  https://life.bio.sunysb.edu/morph/\n\nInstallation\n============\nThe primary way to install is from pip::\n\n    pip install py_tps\n\nInstallation from source is managed via poetry. https://pypi.org/project/poetry/\nSource can be obtained from https://gitlab.com/ryan-feather/py_tps\n\nTo install, first install poetry.\n\n*Note for conda users*\n\nIn order to use a conda environment with poetry, you must first configure poetry to use your conda environment and\nnot create a new virtualenv environment. Example::\n\n    poetry config settings.virtualenvs.path $CONDA_ENV_PATH\n    poetry config settings.virtualenvs.create 0\n\nThen run::\n\n  poetry install\n  poetry build\n  cd dist\n  pip install *.whl\n\nUsage\n=====\n::\n\n    from py_tps import TPSFile, TPSImage, TPSCurve, TPSPoints\n    import numpy as np\n\n    # construct and write\n    # numpy is used for numeric data\n    points = TPSPoints(np.asarray([[33,44],\n                                   [44,45]]))\n    curve = TPSCurve(points)\n    image = TPSImage(\'T1.JPG\', curves=[curve], id_number=0, comment="This is a test", scale=0.0045)\n    tps_file = TPSFile([image]) # can have many images, but here we do just one\n    tps_file.write_to_file(\'TestFile.TPS\')\n\nCreates a file with the contents::\n\n    LM=0\n    CURVES=1\n    POINTS=2\n    33 44\n    44 45\n    IMAGE=T1.JPG\n    ID=0\n    COMMENT=This is a test\n    SCALE=0.0045\n\n\nNow to read::\n\n    tps_file_in =TPSFile.read_file(\'TestFile.TPS\')\n    # now can access images list, and so on.  Attributes have the same names as they do in the objects above.\n    print(tps_file.images[0].image) # T1.JPG\n    print(tps_file.images[0].curves[0].tps_points.points) # [[33,44],[44,45]]\n\nLandmarks can be set instead of or with curves. If we instead do::\n\n        image = TPSImage(\'T1.JPG\', landmarks=points, id_number=0, comment="This is a test", scale=0.0045)\n\nIt creates the file with contents::\n\n    LM=2\n    33 44\n    44 45\n    IMAGE=T1.JPG\n    ID=0\n    COMMENT=This is a test\n    SCALE=0.0045\n',
    'author': 'ryanfeather',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
