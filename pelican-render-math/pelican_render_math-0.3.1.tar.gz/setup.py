"""Setup file
"""


import setuptools
import pelican_render_math


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='pelican_render_math',
                 version=pelican_render_math.__version__,
                 description='Pelican math rendering plugin modified to work with nice-blog theme',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url=pelican_render_math.__github_url__,
                 author='James W. Kennington',
                 author_email='jameswkennington@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False, 
                 include_package_data=True)
