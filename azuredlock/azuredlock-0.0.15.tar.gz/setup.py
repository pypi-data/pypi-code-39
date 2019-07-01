from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='azuredlock',
    py_modules=['azuredlock', 'role'],
    version='0.0.15',
    install_requires=['click', 'requests'],
    python_requires='~=3.5',
    url='',
    license='MIT',
    author='cloudcraeft',
    author_email='cloudcraeft@outlook.com',
    description='azure + redlock',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'azuredlock = azuredlock:cli'
        ]
    }
)
