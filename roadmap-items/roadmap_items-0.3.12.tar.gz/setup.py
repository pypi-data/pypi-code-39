from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='roadmap_items',
      version='0.3.12',
      description='Roadmap service to manage roadmaps and roadmap items with RBAC',
      url='https://wittlesouth.com:32002/projects/RFTW/repos/roadmap_items/browse',
      author='Wittle South Ventures, LLC',
      author_email='eric@wittlesouth.com',
      classifiers= ['License :: Other/Proprietary License', 'Intended Audience :: Developers', 'Topic :: Software Development :: Libraries'],
      packages=['roadmap_items', 'roadmap_items/cli'],
      include_package_data=True,
      data_files=[('spec', ['src/spec/roadmap_items.yaml'])],
      install_requires=[
          'coverage',
          'nose',
          'PyYAML',
          'smoacks'
          ],
      entry_points={
          'console_scripts': [
              'rs_add_roadmap=roadmap_items.cli.add_roadmap:add',
              'rs_import_roadmap=roadmap_items.cli.imp_roadmap:import_csv',
              'rs_search_roadmap=roadmap_items.cli.search_roadmap:search',
              'rs_add_roadmap_auth=roadmap_items.cli.add_roadmap_auth:add',
              'rs_import_roadmap_auth=roadmap_items.cli.imp_roadmap_auth:import_csv',
              'rs_add_roadmap_item=roadmap_items.cli.add_roadmap_item:add',
              'rs_import_roadmap_item=roadmap_items.cli.imp_roadmap_item:import_csv',
              'rs_search_roadmap_item=roadmap_items.cli.search_roadmap_item:search',
              
          ]
      },
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)