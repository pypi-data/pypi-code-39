# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.vision import face_register


def face_register_sample(face_path):
    """
        人脸注册程序
        face_path:人脸库路径
    """
    print('人脸注册开始......')
    res = face_register(face_path=face_path)
    if res is True:
        print('人脸注册成功!')
    else:
        print('人脸注册失败!')
    return res


if __name__ == '__main__':
    print('>>> 输入路径不能有中文 <<<')
    face_path_ = input('请输入人脸库所在路径:')
    face_register_sample(face_path_)
