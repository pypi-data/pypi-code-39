from setuptools import setup


setup(
    name='irl2019',
    version='0.7',
    description='Temporary package to support an event.',
    url='',
    author='Matthew Honnibal',
    author_email='matt@explosion.ai',
    license='MIT',
    packages=['irl2019'],
    setup_requires=["spacy>=2.1.4", "google_cloud_storage"],
    zip_safe=False
)
