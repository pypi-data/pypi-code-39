from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
  name='automate-django',
  packages=find_packages(),
  version='0.1.2',
  license='MIT',
  description='Useful tool to create a static running django application Python',
  long_description_content_type="text/markdown",
  long_description=README + '\n\n' + HISTORY,
  author='Syed Khizaruddin',
  author_email='khizaruddins@gmail.com',
  url='https://github.com/khizaruddins/automate-django',
  keywords=['Django', 'Automation', 'DjangoAutomation', 'AutomateDjango', 'DjangoAutomate', 'AutomationDjango'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)