# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zoloto', 'zoloto.cameras']

package_data = \
{'': ['*'], 'zoloto': ['cli/*']}

install_requires = \
['cached-property>=1.5,<2.0',
 'coordinates>=0.3.0,<0.4.0',
 'fastcache>=1.1,<2.0',
 'opencv-contrib-python-headless>=4.1,<5.0',
 'ujson>=1.35,<2.0']

extras_require = \
{'rpi': ['picamera[array]>=1.13,<2.0']}

entry_points = \
{'console_scripts': ['zoloto-calibrate = zoloto.cli.calibrate:main',
                     'zoloto-preview = zoloto.cli.preview:main']}

setup_kwargs = {
    'name': 'zoloto',
    'version': '0.2.0',
    'description': 'A fiducial marker system powered by OpenCV - Supports ArUco and April',
    'long_description': '# Zoloto\n\n[![Build Status](https://travis-ci.com/RealOrangeOne/zoloto.svg?token=QfVqsaDMCvXipuMx4b2z&branch=master)](https://travis-ci.com/RealOrangeOne/zoloto)\n![PyPI](https://img.shields.io/pypi/v/zoloto.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoloto.svg)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/zoloto.svg)\n![PyPI - Status](https://img.shields.io/pypi/status/zoloto.svg)\n![PyPI - License](https://img.shields.io/pypi/l/zoloto.svg)\n\nA fiducial marker system powered by OpenCV - Supports ArUco and April\n\n## Installation\n\n```\npip install zoloto\n```\n\n## Examples\n\n```python\nfrom pathlib import Path\n\nfrom zoloto import MarkerDict\nfrom zoloto.cameras import ImageFileCamera\n\nwith ImageFileCamera(Path("my-image.png"), marker_dict=MarkerDict.DICT_6X6_50) as camera:\n    camera.save_frame("my-annotated-image.png", annotate=True)\n    print("I saved an image with {} markers in.".format(len(camera.get_visible_markers())))\n```\n\nMore examples can be found in the [`examples/`](https://github.com/RealOrangeOne/zoloto/tree/master/examples) directory.\n',
    'author': 'Jake Howard',
    'author_email': 'git@theorangeone.net',
    'url': 'https://github.com/RealOrangeOne/zoloto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
