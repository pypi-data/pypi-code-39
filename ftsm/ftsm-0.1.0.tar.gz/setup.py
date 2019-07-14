import setuptools

setuptools.setup(name='ftsm',
                 version='0.1.0',
                 description='A Finite Transactional State Machine.',
                 long_description_content_type="text/markdown",
                 long_description=open('README.md').read().strip(),
                 author='Ketan Patel',
                 author_email='ketan86ecer@gmail.com',
                 url='https://github.com/ketan86/ftsm',
                 packages=['ftsm'],
                 install_requires=[],
                 license='MIT License',
                 keywords='ftsm package',
                 classifiers=[
                     "License :: OSI Approved :: MIT License",
                     "Programming Language :: Python :: 3.6",
                     "Programming Language :: Python :: 3.7",
                 ])
