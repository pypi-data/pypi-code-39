import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

required_packages=[
    'google-cloud-logging>=1.10.0',
    'google-cloud-datastore>=1.8.0',
    'google-cloud-bigquery>=1.16.0',
    'google-cloud-storage>=1.15.0',
    'gcsfs>=0.1.2',
    'pyarrow>=0.12.1 ',
    'pandas>=0.24.1',
    'redis>=3.0.1'
]

setuptools.setup(
    name="mms-pip",
    version="0.8.0",
    author="Josef Goppold, Tobias Hoke",
    author_email="goppold@mediamarktsaturn.com, hoke@mediamarktsaturn.com",
    description="A custom MMS/GDWH module for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://source.cloud.google.com/v135-5683-alice-ksk-explore/mms-pip",
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
