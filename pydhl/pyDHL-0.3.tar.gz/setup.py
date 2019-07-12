from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='pyDHL',
    version='0.3',
    packages=['pyDHL'],
    description='DHL REST Webservice integration',
    long_description=readme(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    zip_safe=False,
    entry_points = {
      'console_scripts': ['pyDHL=pyDHL.command_line:main'],
    },
    author='SMACH Team',
    maintainer_email='pablo.riutort@smachteam.com',
)
