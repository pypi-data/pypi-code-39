import pathlib

from setuptools import setup

setup(
    name='fxq-ae-agent',
    version='0.0.15',
    packages=[
        'fxq.ae.agent',
        'fxq.ae.agent.callback',
        'fxq.ae.agent.factory',
        'fxq.ae.agent.model',
        'fxq.ae.agent.service',
    ],
    url='https://bitbucket.org/fxquants/ae-agent/',
    license='MIT',
    author='Jonathan Turnock',
    author_email='jonathan.turnock@fxquants.net',
    description='Analytics Engine Agent Client, Provisions and executes docker pipelines from git repo yml',
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=[
        'docker',
        'flask',
        'fxq-core',
        'gitpython',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': ['fxq-ae-agent=fxq.ae.agent.cli:main'],
    }
)
