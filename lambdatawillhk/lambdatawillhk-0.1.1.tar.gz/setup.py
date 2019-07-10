from distutils.core import setup
setup(
    name='lambdatawillhk',
    packages=['lambdatawillhk'],
    version='0.1.1',
    license='MIT',
    description='collection of dataframe functions',
    author='Will Haeck',
    author_email='will.haeck@gmail.com',
    url='https://github.com/willhk/lambdatawillhk',
    # download_url = '',
    keywords = ['pandas', 'null checking'],
    install_requires=[
        'pandas'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
)