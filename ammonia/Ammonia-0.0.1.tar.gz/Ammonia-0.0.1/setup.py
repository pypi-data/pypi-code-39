from setuptools import setup

with open('requirements.txt', encoding='utf-8') as f:
    requirements = list(filter(None, [x for x in f.read().splitlines()]))

setup(
    name="Ammonia",
    version="0.0.1",
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
