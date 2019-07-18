#coding=utf-8
from distutils.core import setup

setup(
    name='baizhanSuperMath3',  #对外我们模块的名称
    version='3.7',  #版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试',  #描述
    author='zhanghaixuan',  #作者
    author_email='316256501@qq.com',
    py_modules=['baizhanSuperMath3.demo1','baizhanSuperMath3.demo2']   #要发布的模块
)