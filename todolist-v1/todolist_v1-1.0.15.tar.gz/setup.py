import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='todolist_v1',
    version='1.0.15',
    packages=find_packages(),
    include_package_data=True,
    description='A simple Django app to keep track of your todo list. It comes with a RESTful API, celery task queue, Oauth2 and is fully tested.',
    long_description=open('README.md').read(),
    author='Kenneth Mathenge',
    author_email='mathenge@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "Django==2.2.3",
        "celery==3.1.18",
        "django-allauth==0.39.1",
        "django-rest-framework==0.1.0",
        "django-environ==0.4.5",
        "psycopg2==2.8.3",
        "gunicorn==19.9.0",
        "django-rest-auth==0.9.5",
        "celery==3.1.18",
        "redis==3.2.1",
        "fabric3==1.14.post1",
    ],
    scripts=['bin/todo_manage'],
)
