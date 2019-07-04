import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-watchful",
    "version": "0.2.1",
    "description": "Watching your CDK apps since 2019",
    "url": "https://github.com/eladb/cdk-watchful",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<elad.benisrael@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/eladb/cdk-watchful"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_watchful",
        "cdk_watchful._jsii"
    ],
    "package_data": {
        "cdk_watchful._jsii": [
            "cdk-watchful@0.2.1.jsii.tgz"
        ],
        "cdk_watchful": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.13.3",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway~=0.36.1",
        "aws-cdk.aws-cloudwatch~=0.36.1",
        "aws-cdk.aws-cloudwatch-actions~=0.36.1",
        "aws-cdk.aws-dynamodb~=0.36.1",
        "aws-cdk.aws-events~=0.36.1",
        "aws-cdk.aws-events-targets~=0.36.1",
        "aws-cdk.aws-lambda~=0.36.1",
        "aws-cdk.aws-sns~=0.36.1",
        "aws-cdk.aws-sns-subscriptions~=0.36.1",
        "aws-cdk.core~=0.36.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
