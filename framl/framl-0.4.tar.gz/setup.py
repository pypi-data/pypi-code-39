from setuptools import setup

setup(
    name='framl',
    version='0.4',
    description='Frame to create ML predictor and trainer',
    url='',
    author='Machavia Pichet',
    author_email='machavia.pichet@blablacar.com',
    license='MIT',
    packages=['framl'],
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/framl'],
)
