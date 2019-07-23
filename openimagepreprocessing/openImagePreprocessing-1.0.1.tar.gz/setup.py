from setuptools import setup
from setuptools import find_packages
 
setup(
    name='openImagePreprocessing',
    version='1.0.1',
    description='Preprocess functions for the Open Image Dataset.',
    packages=find_packages(),
    author='zhenwan,t-zhiwan,t-tozho',
    author_email='zhenwan@microsoft.com,t-zhiwan@microsoft.com,t-tozho@microsoft.com',
    url='https://dev.azure.com/zhenwan/zhenwan_default/_git/AMLProjects',
    install_requires=[
        'pandas',
        'numpy',
        'azure-storage-blob',
        'opencv-contrib-python',
        'Pillow'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
