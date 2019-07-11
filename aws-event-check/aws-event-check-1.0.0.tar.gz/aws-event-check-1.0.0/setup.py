from setuptools import setup

with open("README.md", "r") as readme:
    description = readme.read()

with open("LICENSE", "r") as readme:
    license_x = readme.read()

license_x_y = " : ".join(x for x in license_x.split("\n")[:3] if x)

description = "{} \n\n {}".format(description, license_x_y)

setup(
    name='aws-event-check',
    version='1.0.0',
    packages=[],
    url='https://github.com/AbhimanyuHK/AWS-Event-Check',
    license=license_x_y,
    author='Abimanyu H K',
    author_email='manyu1994@hotmail.com',
    description='A Event Checker For AWS Lambda Handler.',
    long_description=description,
    long_description_content_type="text/markdown"
)
