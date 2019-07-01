import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.assets",
    "version": "0.36.1",
    "description": "Integration of CDK apps with local assets",
    "url": "https://github.com/awslabs/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.assets",
        "aws_cdk.assets._jsii"
    ],
    "package_data": {
        "aws_cdk.assets._jsii": [
            "assets@0.36.1.jsii.tgz"
        ],
        "aws_cdk.assets": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.13.2",
        "publication>=0.0.3",
        "aws-cdk.core~=0.36.1",
        "aws-cdk.cx-api~=0.36.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
