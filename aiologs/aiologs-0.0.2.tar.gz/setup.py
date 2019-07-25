from setuptools import setup, find_packages

setup(
    name='aiologs',
    version='0.0.2',
    description=(
        '纯异步的高性能日志组件，支持日志保存文件、mongo、elasticsearch',
        'Purely asynchronous high performance logging components，Support for writing files，mongo、elasticsearch'
    ),
    long_description=open('README.rst','rb').read(),
    author='beincy',
    author_email='bianhui0524@sina.com',
    maintainer='卞辉(beincy)',
    maintainer_email='bianhui0524@sina.com',
    license='MIT',
    packages=['aiologs'],
    platforms=["all"],
    url='https://github.com/beincy/aiologs',
    install_requires=[
        'uvloop',
        'motor',
        'elasticsearch-async',
        'ujson',
        'aiofiles',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)