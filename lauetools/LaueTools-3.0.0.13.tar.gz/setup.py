from setuptools import setup, find_packages
setup(
    name="LaueTools",
    version="3.0.0.13",
packages=find_packages(),
#     packages=['LaueToolsRev2231'],
    #packages=find_packages(exclude=('LaueTools',)),

    python_requires='>=2.6 , <3.7',

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3',
                      'numpy>=1.11.3',
                      'scipy>=0.19.0',
                      'matplotlib>=2.0.0',
                      'wxpython>=3.0',
                      'networkx>=2.1'],

include_package_data=True,

    #package_data={'lauetools-master': ['*.py','*.txt','*.mccd','*.tif','*.tiff','*.dat','*.cor','*.det','*.png','*.rst','*.yml','*.ipynb']
    #},
#         # If any package contains *.txt or *.rst files, include them:
#         '': ['*.txt', '*.rst'],
#         # And include any *.msg files found in the 'hello' package, too:
#         'hello': ['*.msg'],
#     },

    # metadata for upload to PyPI
    author="J S Micha",
    author_email="micha@esrf.fr",
    description="First trials to distribute LaueTools Package with pip",
    license="MIT",
    keywords="Lauetools x-ray scattering data analysis GUI Laue",
    url="https://sourceforge.net/projects/lauetools/",  # project home page, if any
    classifiers=[
        "Programming Language :: Python :: 3.6",
	"Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
	"Programming Language :: Python :: 2.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # could also include long_description, download_url, classifiers, etc.
)
