from distutils.core import setup
setup(
    name='entityinfo',         # How you named your package folder (MyLib)
    packages=['entityinfo'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='With entityinfo, you can extract information correct and full entity name',
    author='ravindersingh',                   # Type in your name
    author_email='ravinderkhatri@outlook.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/ravinderkhatri/entityinfo',
    # I explain this later on
    download_url='https://github.com/ravinderkhatri/entityinfo/archive/v01.tar.gz',
    # Keywords that define your package best
    keywords=['EntityName', 'EntityInformation',
              'RawName to Business Name', 'Trasactional Info'],
    install_requires=[
        'abbreviations',
        'collections',
        'fuzzywuzzy',
        'itertools',
        'pandas'
        'python-Levenshtein',
        'tldextract',
        'spacy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
