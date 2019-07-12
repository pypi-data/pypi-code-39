# -*- coding: utf-8 -*-
"""Setup module for flask taxonomy."""

from setuptools import setup

install_requires = [
    'Flask>=1.0.3',
    'Werkzeug>=0.15.4',
    'webargs>=5.3.2',
    'Flask-Alembic>=2.0.1',
    'Flask-SQLAlchemy>=2.4.0',
    'SQLAlchemy>=1.3.5',
    'sqlalchemy_mptt>=0.2.4',
]

setup(
    name="flask_taxonomies",
    version="2.0.0",
    url="https://github.com/oarepo/flask-taxonomies",
    license="MIT",
    author="Miroslav Bauer",
    author_email="bauer@cesnet.cz",
    description="Taxonomy Term trees REST API for Flask Applications",
    zip_safe=False,
    packages=['flask_taxonomies'],
    entry_points={
        'invenio_db.models': [
            'flask_taxonomies = flask_taxonomies.models',
        ],
        'invenio_db.alembic': [
            'flask_taxonomies = flask_taxonomies:alembic',
        ]
    },
    include_package_data=True,
    install_requires=install_requires,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
    ],
)
