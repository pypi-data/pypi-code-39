import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-dynamo-table-viewer",
    "version": "3.0.1",
    "description": "cdk-dynamo-table-viewer",
    "url": "https://github.com/eladb/cdk-dynamo-table-viewer.git",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<elad.benisrael@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/eladb/cdk-dynamo-table-viewer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_dynamo_table_viewer",
        "cdk_dynamo_table_viewer._jsii"
    ],
    "package_data": {
        "cdk_dynamo_table_viewer._jsii": [
            "cdk-dynamo-table-viewer@3.0.1.jsii.tgz"
        ],
        "cdk_dynamo_table_viewer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.14.0",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway~=0.38.0",
        "aws-cdk.aws-dynamodb~=0.38.0",
        "aws-cdk.aws-lambda~=0.38.0",
        "aws-cdk.core~=0.38.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
