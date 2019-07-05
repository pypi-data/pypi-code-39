from setuptools import setup

setup(
    name='okeydokey',
    version='0.1.0',
    packages=['okeydokey', 'okeydokey.notifier'],
    url='https://github.com/droberin/notary',
    license='MIT',
    author='Roberto Salgado',
    author_email='drober@gmail.com',
    description='Notify on shared password retrieval',
    install_requires=[
        'cryptography>=2.*',
        'Flask>=1.*',
        'python-telegram-bot>=10.*',
        'pyyaml>=5.*'
    ],
)
