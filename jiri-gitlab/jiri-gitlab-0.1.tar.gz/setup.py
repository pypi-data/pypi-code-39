from setuptools import setup

setup(
    name='jiri-gitlab',
    version='0.1',
    packages=['jiri_gitlab'],
    url='https://gitlab.com/tom6/jiri-gitlab',
    license='MIT',
    author='Tom Forbes',
    author_email='tom@tomforb.es',
    description='A tool to create a Jiri manifest file from Gitlab projects',
    install_requires=[
        'python-gitlab',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jiri-gitlab = jiri_gitlab.cli:create_manifest',
            'jiri-list = jiri_gitlab.cli:list_projects',
        ],
    }
)
