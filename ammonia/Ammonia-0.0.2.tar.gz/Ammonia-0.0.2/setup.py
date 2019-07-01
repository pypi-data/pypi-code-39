from setuptools import setup
import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    requirements = list(filter(None, [x for x in f.read().splitlines()]))

setup(
    name="Ammonia",
    version="0.0.2",
    description="task queue",
    author="george wang",
    author_email="georgewang1994@163.com",
    url="https://github.com/GeorgeWang1994/Ammonia",
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            'ammonia=ammonia.command.start:start'
        ],
    },
)
