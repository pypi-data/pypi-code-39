from distutils.core import setup

setup(
    name = 'myFirstPackage_01_GARCIA', #对外模块的名字
    version = '1.0',  #发布的版本号
    description= '对外发布的模块，仅有加法和乘法，用于测试',
    author= 'jane', #作者
    author_email= '123456789@qq.com', #邮箱
    py_modules=['myFirst01', 'myFirst02'] #要发布的模块
)