from distutils.core import setup


setup(
    name="BruceTang",     #对外我们模块的名字
    version = '1.0',        # 版本号
    description='这是第一个对外发布的模块，', # 描述
    author= "quantbruce",
    author_email= "quantbruce@qq.com",
    py_modules=['baizhanSuperMath.demo1', 'baizhanSuperMath.demo2']  # 要发布的模块
)

