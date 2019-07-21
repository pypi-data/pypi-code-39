from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'Package for Working with Factors' 
  
setup( 
        name ='math-factors', 
        version ='1.0.1', 
        author ='Prateek C. Tripathi', 
        author_email ='prateektripathi85@gmail.com', 
        url ='https://github.com/Prateek23n/Factors', 
        description ='Demo Package for Mathematical Factors.', 
         long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(exclude=['contrib', 'docs', 'tests*']), 
        entry_points ={ 
            'console_scripts': [ 
                
            ] 
        },
        python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
        classifiers=(
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
), 
        keywords ='python factors', 
        install_requires = requirements, 
        zip_safe = True
)
