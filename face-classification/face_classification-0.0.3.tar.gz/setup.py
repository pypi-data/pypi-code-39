from setuptools import setup

# TODO: More informative metadata creation

setup(
    name='face_classification',
    version='0.0.3',
    description='Train and classifiy faces from images using deep learning. https://gitlab.lftechnology.com/leapfrogai/face-classification/',
    author='Leapfrog Technology INC',
    author_email='hello@lftechnology.com',
    license='Apache License 2.0',
    packages=['face_classification'],
    install_requires=[
          'face_recognition',
          'sklearn'
      ],
    zip_safe=False
)
