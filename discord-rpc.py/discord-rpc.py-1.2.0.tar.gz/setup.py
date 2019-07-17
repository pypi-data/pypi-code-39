import setuptools
from discord_rpc import VERSION, PROJECT_URL
from discord_rpc.util.utils import is_python3

with open("README.md", "r") as fh:
    long_description = fh.read()

# I hate having to use dependencies if I don't really need to for this library...
install_dependencies = list()
if not is_python3():
    install_dependencies.append('requests')

setuptools.setup(
    name="discord-rpc.py",
    url=PROJECT_URL,
    version=VERSION,
    author="Gustavo (somberdemise)",
    author_email="me@gustavo.dev",
    description="A Discord Rich Presence library for Python 2 & 3",
    license='Mozilla Public License 2.0 (MPL 2.0)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'discord_rpc',
        'discord_rpc.codes',
        'discord_rpc.connection',
        'discord_rpc.util'
    ],
    platforms=[
        'Windows',
        'Linux',
        'OSX'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",

        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=install_dependencies,
)
