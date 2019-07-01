#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['NetTrade',
 'NetTrade.ExcelDataUtil',
 'NetTrade.HistoryNotes',
 'NetTrade.Notes',
 'NetTrade.Strategy',
 'NetTrade.TestDataUtil',
 'NetTrade.Util',
 'NetTrade.Variables']

package_data = \
{'': ['*']}

install_requires = \
['idataapi-transform', 'requests']

setup(name='NetTrade',
      version='1.0.3',
      description='NetTrade tools',
      author='zpoint',
      author_email='zp@zp0int.com',
      url='https://github.com/zpoint/NetTrade',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      python_requires='>=3.5.2',
     )
