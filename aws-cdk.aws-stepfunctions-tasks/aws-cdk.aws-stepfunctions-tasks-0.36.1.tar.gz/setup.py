import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-stepfunctions-tasks",
    "version": "0.36.1",
    "description": "Task integrations for AWS StepFunctions",
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
        "aws_cdk.aws_stepfunctions_tasks",
        "aws_cdk.aws_stepfunctions_tasks._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_stepfunctions_tasks._jsii": [
            "aws-stepfunctions-tasks@0.36.1.jsii.tgz"
        ],
        "aws_cdk.aws_stepfunctions_tasks": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.13.2",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudwatch~=0.36.1",
        "aws-cdk.aws-ec2~=0.36.1",
        "aws-cdk.aws-ecs~=0.36.1",
        "aws-cdk.aws-iam~=0.36.1",
        "aws-cdk.aws-kms~=0.36.1",
        "aws-cdk.aws-lambda~=0.36.1",
        "aws-cdk.aws-sns~=0.36.1",
        "aws-cdk.aws-sqs~=0.36.1",
        "aws-cdk.aws-stepfunctions~=0.36.1",
        "aws-cdk.core~=0.36.1"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
