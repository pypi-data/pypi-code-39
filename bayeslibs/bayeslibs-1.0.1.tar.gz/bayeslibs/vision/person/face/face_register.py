# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/21
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import base64
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request
import cv2
import os
import numpy
from aip import AipFace


class BayesFaceRegister:
    __APP_ID = '14987471'
    __API_KEY = '5T5yB8G2OpFdCcVb1OK7ipap'
    __SECRET_KEY = 'juNdil9rcizpakslmUXSHRQzuo9h0T96'
    __GROUP_ID = 'bayes_test'
    __TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

    def __init__(self):
        self.aip_client = AipFace(self.__APP_ID, self.__API_KEY, self.__SECRET_KEY)
        super().__init__()

    def token_acquire(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.__API_KEY,
                  'client_secret': self.__SECRET_KEY}
        post_data = urlencode(params).encode('utf-8')
        req_ = Request(self.__TOKEN_URL, post_data)
        try:
            f_ = urlopen(req_, timeout=5)
            result_str_ = f_.read().decode('utf-8')
            res = json.loads(result_str_)
            f_.stop()
            if 'access_token' in res:
                return res['access_token']
            else:
                raise Exception('access_token not in result')
        except Exception as err:
            print('BayesFaceRecognize token_acquire failed: {}'.format(err))
            return None

    @staticmethod
    def img2base64(img_src):
        if isinstance(img_src, numpy.ndarray):
            img_str = cv2.imencode('.jpg', img_src)[1].tostring()
            img_base64 = base64.b64encode(img_str).decode('utf-8')
        else:
            img_str = cv2.imencode('.jpg', img_src)[1].tostring()
            img_base64 = base64.b64encode(img_str).decode('utf-8')
        return img_base64

    def register(self, img_src, user_id, group_id=__GROUP_ID):
        img_base64 = self.img2base64(img_src)
        img_type = 'BASE64'
        options = {"user_info": "{}'s info".format(user_id),
                   "quality_control": "NORMAL",
                   "liveness_control": "LOW"}
        return self.aip_client.addUser(img_base64, img_type, group_id, user_id, options)

    def update(self, img_src, user_id, group_id=__GROUP_ID):
        img_base64 = self.img2base64(img_src)
        img_type = 'BASE64'
        options = {"user_info": "{}'s info".format(user_id),
                   "quality_control": "NORMAL",
                   "liveness_control": "LOW"}
        return self.aip_client.updateUser(img_base64, img_type, group_id, user_id, options)

    def delete_face(self, user_id, face_token, group_id=''):
        return self.aip_client.faceDelete(user_id, group_id, face_token)

    def delete_user(self, user_id, group_id):
        return self.aip_client.deleteUser(group_id, user_id)

    def query_face(self, user_id, group_id):
        return self.aip_client.faceGetlist(user_id, group_id)

    def query_user(self, user_id, group_id):
        return self.aip_client.getUser(user_id, group_id)


def face_register(face_path):
    """
    多张人脸图片录入接口
    :param face_path: 多张人脸图片所在的文件夹路径
    :return:
    """
    try:
        if '\u202a' in face_path:
            face_path = face_path[1:]
        dir_files = os.listdir(face_path)
    except FileNotFoundError:
        print('input face path is wrong, please check your path')
        print('程序异常退出!')
        return False
    except OSError as err:
        print('input face path is wrong, please check your path, err:{}'.format(err))
        print('程序异常退出!')
        return False
    bayes_face = BayesFaceRegister()
    for filename in dir_files:
        file_path = '{}'.format(os.path.join(face_path, filename))
        if os.path.isdir(file_path):
            print('input face path is wrong, please check your path')
            continue
        if os.path.isfile(file_path):
            user_id = filename.split('.')[0]
            img_format = filename.split('.')[-1]
            if img_format not in ['png', 'jpg', 'bmp']:
                print('{} is not a supported image format'.format(filename))
                continue
            try:
                img_file = cv2.imread(file_path)
                if img_file is not None:
                    res = bayes_face.register(img_file, user_id=user_id)
                    if res and res['error_code'] == 0:
                        print('{} register success'.format(user_id))
                    else:
                        print('{} register failed, error:{}'.format(user_id, res['error_msg']))
                        continue
                else:
                    print('{} can\'t be read by opencv, please check your input path'.format(filename))
                    print('程序异常退出!')
                    return False
            except Exception as err:
                print('{} register failed, error:{}'.format(user_id, err))
                print('程序异常退出!')
                return False
    print('all image register finished')
    return True


def face_register_img(img_path):
    """
    单张人脸图片录入接口
    :param img_path:人脸图片路径
    :return:
    """
    if not os.path.isfile(img_path):
        print('input face path is wrong, please check your path')
        return False
    filename = os.path.basename(img_path)
    img_format = filename.split('.')[-1]
    if img_format not in ['png', 'jpg', 'bmp']:
        print('{} is not a supported image format'.format(filename))
        return False
    bayes_face = BayesFaceRegister()
    user_id = filename.split('.')[0]
    img_file = cv2.imread(img_path)
    res = bayes_face.register(img_file, user_id=user_id)
    if res and res['error_code'] == 0:
        print('{} register success'.format(user_id))
    else:
        print('{} register failed:{}'.format(user_id, res['error_msg']))
    return True


if __name__ == '__main__':
    # t1 = time.clock()
    face_register_img('./huge.jpg')
    print(os.path.isfile('../face/huge.jpg'))
