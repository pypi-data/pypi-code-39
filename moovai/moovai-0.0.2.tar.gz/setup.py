from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="moovai",
    version="0.0.2",
    packages=find_packages(),
    scripts=['moovai/test.py', 'moovai/google_cloud/cloud_storage.py', 'moovai/google_cloud/bigquery.py'],
    install_requires=[
        "google-cloud-error-reporting==0.28.0",
        "google-cloud-bigquery==0.29.0",
        "google-cloud-storage==1.6.0",
        "joblib",
        "pandas"
    ],

    author="Antsa Randriamihaja",
    author_email="antsa.randriamihaja@moov.ai",
    description="A package for working with GCS and BigQuery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moovai/Toolbox/",
    project_urls={
        "Documentation": "https://github.com/moovai/Toolbox/blob/master/README.md",
        "Source Code": "https://github.com/moovai/Toolbox/tree/master/MoovAI",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)