# -*- coding: utf-8 -*-
"""Installer for the collective.portlet.existingcontent package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.portlet.existingcontent',
    version='1.0.2',
    description="Existing Content Portlet",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Markus Hilbert',
    author_email='markus.hilbert@iham.at',
    url='https://github.com/collective/collective.portlet.existingcontent',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.portlet'],
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        'Products.CMFPlone',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.portlet.existingcontent.locales.update:update_locale
    """,
)
