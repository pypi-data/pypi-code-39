from setuptools import setup, find_packages

with open('README.md', 'r') as in_:
    long_description = in_.read()

setup(
    name='deploynow',
    author='Anushka Yohan',
    author_email='anushka.yohan@pearson.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    long_description= 'long_description',
    long_description_content_type='text/markdown',
    url='https://github.com/AnushkaYohan/code-deploy-now',
    install_requires=['boto3'],
    packages=find_packages(),
    include_package_data=True,
    version="1.10.0",
    scripts=['deploynow']
)
