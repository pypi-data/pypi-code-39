from setuptools import setup, find_packages
setup(
        name='PushTool',     # 包名字
        version='1.1',   # 包版本
        description='push tool can help your work',   # 简单描述
        author='Mryan2005',  # 作者
        author_email='A2564011261@163.com',  # 作者邮箱
        url='https://github.com/SuperSystemStudio/push.bat.git',      # 包的主页
        license='MIT License',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=True,
        entry_points={
            'console_scripts':[
                'push = pushtool.push:main'
            ]
        },
)