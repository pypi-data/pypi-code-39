from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
      name="dharma-callback-fuzzer",
      version="1.2.1",
      description="Generation-based, context-free grammar fuzzer dharma (callback fuzzer).",
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/pjiajun/dharma-callback-fuzzer.git",
      author="Jiajun Peng",
      author_email="jiajunp@fb.com",
      license="MPL 2.0",
      classifiers=[
                   "Topic :: Software Development :: Testing",
                   "Topic :: Security",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)"
                   ],
      packages=["dharma_callback_fuzzer"],
      include_package_data=True,
      install_requires=["requests"],
      entry_points={
      "console_scripts": [
                          "dharma-callback-fuzzer=dharma_callback_fuzzer.harness:main",
                          ]
      },
      )
