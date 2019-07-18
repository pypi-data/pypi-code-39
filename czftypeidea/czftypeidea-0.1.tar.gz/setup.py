from setuptools import setup, find_packages

setup(
    name='czftypeidea',
    version='0.1',
    description='Blog System base on Django',
    author='czf34',
    author_email='czf34@163.com',
    url='https://www.the5fire.com',
    license = 'MIT',
    packages=find_packages('typeieda'),
    package_dir={'': 'typeidea'},
    package_data={'': [
        'themes/*/*/*/*',
    ]},
    install_requires=[
        'django==1.11',
    ],
    extra_require={
        'ipython': ['ipython==6.2.1']
    },
    scripts=[
        'typeidea/manage.py',
    ],
    entry_points={
        'console_scripts': [
            'typeidea_manage = manage:main',
        ]
    },
    classifiers=[
        # 软件成熟度
        'Development Status :: 3 - Alpha',
        
        # 指明项目的受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        
        # 选择项目的许可证(License)
        'License :: OSI Approved :: MIT License',
        
        # 指定项目需要使用的Python版本
        'Programming Language :: Python :: 3.7',
    ],
)