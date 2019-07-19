
from setuptools import setup

setup(
    name='dingtalk-webhook',
    version='1.0',
    keywords='dingtalk, dingding, dingtalk-webhook, ding, alert',
    description='send dingtalk message to dingding webhook robot',
    py_modules=['dingtalk-webhook'],
    author='zhanghe',
    author_email='x_hezhang@126.com',
    license='GNU GPLv3',
    install_requires=[
        'requests'
    ],
    packages=[
        'dingtalk-webhook'
    ]
)
