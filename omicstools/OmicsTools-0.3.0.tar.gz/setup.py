from setuptools import setup, find_packages

setup(
    name='OmicsTools',
    packages=find_packages(),
    package_data={'OmicsTools': ['OmicsTools/enrich/db/go-basic.pkl', 'OmicsTools/enrich/db/symbol2go.pkl']},
    version='0.3.0',
    url='https://github.com/fraenkel-lab/OmicsTools',
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'],
    license='MIT',
    author='iamjli',
    author_email='iamjli@mit.edu',
    description='',
    install_requires=[
        "pandas==0.24.2", 
        "numpy==1.16.4",
        "networkx==2.3",
        "mygene==3.1.0", 
        "goenrich==1.11"
    ]
)