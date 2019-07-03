# -*- coding: utf-8 -*-

from distutils.core import setup
 
setup(
	  name="lt_test", #模块的名称
	  version="1.0",#版本号，每次修改代码的时候，可以改一下
	  description="发布测试的模块",#描述
	  author="tyrone",#作者
	  author_email="tyrone_l@163.com",#联系邮箱
	  url="http://ww.baidu.com",#你的主页
	  py_modules=['lt_test.my_test','lt_test.my_python']#这个是下面有哪些模块可以用
	  )
