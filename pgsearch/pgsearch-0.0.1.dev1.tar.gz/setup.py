from setuptools import setup

setup(
    name='pgsearch',
    version='0.0.1.dev1',
    description='Parallel grid search.',
    url='https://github.com/Tigeraus/pgs',
    author='Huzi Cheng',
    author_email='hzcheng15@icloud.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='grid search optimization model selection',
    packages=['pgsearch'],
    install_requires=['ipython>=7.0']
)
