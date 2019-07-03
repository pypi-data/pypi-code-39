import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(
    name='django_live_notification',
    version='0.0',
    packages=['django_live_notification'],
    description='Real Time Django Notification Library',
    long_description=README,
    author='Ümit Öztürk',
    author_email='umit.ozturk.9716@gmail.com',
    url='https://github.com/umit-ozturk/django-notification',
    license='MIT',
    install_requires=[
        'Django>=1.6,<1.7',
    ]
)