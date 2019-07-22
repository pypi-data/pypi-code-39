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
import os


class BayesFaceRegister:
    __APP_ID = '14987471'
    __API_KEY = '5T5yB8G2OpFdCcVb1OK7ipap'
    __SECRET_KEY = 'juNdil9rcizpakslmUXSHRQzuo9h0T96'
    __GROUP_ID = 'bayes_test'
    __IMAGE_TYPE = 'BASE64'
    __TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
    __USER_ADD_URL = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add'
    __USER_UPDATE_URL = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update'
    __USER_DELETE_URL = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete'
    __USER_GET_URL = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get'

    def __init__(self):
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
            f_.close()
            if 'access_token' in res:
                return res['access_token']
            else:
                raise Exception('access_token not in result')
        except Exception as err:
            print('BayesFaceRecognize token_acquire failed: {}'.format(err))
            return None

    @staticmethod
    def img2base64(img_src):
        try:
            with open(img_src, 'rb') as f:
                b64_data = base64.b64encode(f.read())
            return b64_data
        except Exception as err:
            print('img open failed:{}'.format(err))
            return None

    def http_request(self, request_url, params):
        access_token = self.token_acquire()
        if access_token:
            request_url = '{}?access_token={}'.format(request_url, access_token)
            request = Request(url=request_url, data=params)
            request.add_header('Content-Type', 'application/json')
            response = urlopen(request, timeout=5)
            content = response.read().decode('utf-8')
            response.close()
            if content:
                return json.loads(content)
            else:
                return None
        else:
            return None

    def register(self, img_src, user_id, group_id=__GROUP_ID):
        img_base64 = self.img2base64(img_src)
        if not img_base64:
            return None
        img_type = self.__IMAGE_TYPE
        request_url = self.__USER_ADD_URL
        data = {
            'image': img_base64,
            'image_type': img_type,
            'group_id': group_id,
            'user_id': user_id,
            'user_info': '{}\'s face'.format(user_id)
        }
        params = urlencode(data).encode('utf-8')
        return self.http_request(request_url, params)

    def update(self, img_src, user_id, group_id=__GROUP_ID):
        img_base64 = self.img2base64(img_src)
        if not img_base64:
            return None
        img_type = self.__IMAGE_TYPE
        request_url = self.__USER_UPDATE_URL
        data = {
            'image': img_base64,
            'image_type': img_type,
            'group_id': group_id,
            'user_id': user_id,
            'user_info': '{}\'s face'.format(user_id)
        }
        params = urlencode(data).encode('utf-8')
        return self.http_request(request_url, params)

    def delete_face(self, user_id, face_token, group_id=__GROUP_ID):
        request_url = self.__USER_DELETE_URL
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'face_token': face_token
        }
        params = urlencode(data).encode('utf-8')
        return self.http_request(request_url, params)

    def get_face(self, user_id, group_id=__GROUP_ID):
        request_url = self.__USER_GET_URL
        data = {
            'group_id': group_id,
            'user_id': user_id
        }
        params = urlencode(data).encode('utf-8')
        return self.http_request(request_url, params)


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
                res = bayes_face.register(file_path, user_id=user_id)
                if res and res['error_code'] == 0:
                    print('{} register success'.format(user_id))
                elif res:
                    print('{} register failed:{}'.format(user_id, res['error_msg']))
                    continue
                else:
                    print('发生未知异常错误')
                    continue
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
    res = bayes_face.register(img_path, user_id=user_id)
    if res and res['error_code'] == 0:
        print('{} register success'.format(user_id))
    elif res:
        print('{} register failed:{}'.format(user_id, res['error_msg']))
    else:
        print('发生未知异常错误')
    return True


if __name__ == '__main__':
    face_register_img('./huge.jpg')
