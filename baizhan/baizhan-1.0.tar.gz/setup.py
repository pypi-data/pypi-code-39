from distutils.core import setup
setup(
    name='baizhan', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试用的，嘿嘿~', #描述
    author='huangpu', # 作者
    author_email='huangpu@163.com',
    py_modules=['baizhan.demo1','baizhan.demo2'] # 要发布的模块
)