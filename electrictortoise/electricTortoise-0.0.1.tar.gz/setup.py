import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'electricTortoise',         # How you named your package folder (MyLib)
    version = '0.0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'This package helps determine optimal thrust profiles for space electric propulsion applications. ',   # Give a short description about your library
    author = 'Devansh R Agrawal',                   # Type in your name
    author_email = 'devanshinspace@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/dev10110/electricTortoise',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['Electric Propulsion', 'Optimal Control', 'Preliminary Design'],   # Keywords that define your package best
    packages = setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
