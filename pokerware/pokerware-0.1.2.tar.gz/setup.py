import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='pokerware',
      version='0.1.2',
      description="A small example package",
      long_description_content_type="text/markdown",
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      url='http://github.com/buckley-w-david/Pokerware',
      author='David Buckley',
      author_email='buckley.w.david@gmail.com',
      license='MIT',
      packages=['pokerware'],
      install_requires=[],
      entry_points={
          'console_scripts': ['pokerware=pokerware.cli:main'],
      },
      include_package_data=True,
      zip_safe=False
)
