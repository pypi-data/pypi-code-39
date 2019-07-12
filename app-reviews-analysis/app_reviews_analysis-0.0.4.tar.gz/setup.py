from setuptools import setup,find_packages

# 导入静态文件
# file_data = [
#     "app-reviews-analysis/static"
# ]

# 第三方依赖
requires = [
    "pandas>=0.23.4",
    "nltk>=3.4",
    "seaborn==0.9.0",
    "gensim==3.4.0",
    "emoji==0.5.1",
    "langid==1.1.6"
]

# # 自动读取version信息
# about = {}
# with open(os.path.join(here, 'app-reviews-analysis', '__version__.py'), 'r', 'utf-8') as f:
#     exec(f.read(), about)

# 自动读取readme
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='app_reviews_analysis',  # 包名称
    version='0.0.4',  # 包版本
    description='This library, based on NLTK library and sentience.jar package, is designed to help analyze App comment data, and can implement comment feature extraction, comment emotion analysis, comment star and comment emotion correlation analysis, and comment emotion score prediction',  # 包详细描述
    long_description=readme,   # 长描述，通常是readme，打包到PiPy需要
    long_description_content_type="text/markdown",
    author='lailai',  # 作者名称
    author_email='739198457@qq.com',  # 作者邮箱
    url='',   # 项目官网
    packages=find_packages(),    # 项目需要的包
    include_package_data=True,  # 是否需要导入静态数据文件,启用清单文件MANIFEST.in
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[    # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)