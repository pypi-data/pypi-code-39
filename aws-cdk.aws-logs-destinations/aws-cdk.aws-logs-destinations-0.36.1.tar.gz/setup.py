import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-logs-destinations",
    "version": "0.36.1",
    "description": "Log Destinations for AWS CloudWatch Logs",
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
        "aws_cdk.aws_logs_destinations",
        "aws_cdk.aws_logs_destinations._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_logs_destinations._jsii": [
            "aws-logs-destinations@0.36.1.jsii.tgz"
        ],
        "aws_cdk.aws_logs_destinations": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.13.2",
        "publication>=0.0.3",
        "aws-cdk.aws-iam~=0.36.1",
        "aws-cdk.aws-kinesis~=0.36.1",
        "aws-cdk.aws-lambda~=0.36.1",
        "aws-cdk.aws-logs~=0.36.1",
        "aws-cdk.core~=0.36.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
