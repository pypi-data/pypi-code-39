import setuptools

with open('README.md', 'r') as read_me:
    description = read_me.read()

setuptools.setup(
    name = 'catan-controller',
    version = '0.0.1',
    author = 'James Beringer',
    author_email = 'jamberin@gmail.com',
    description ='Controller for the game Catan',
    long_description = description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/jamberin/Catan',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3'
    ]
)