"""
AI Fashion functions sdk


"""




import os
import sys
import re
from enum import Enum
import json
import base64
import requests
import warnings



from .af_oauth2 import OAuth2GrandTypes, AFOAuth2


URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

TEST_PICTURE_URL = "https://images.aifashion.com/1c/26/fa/1c26fab52ac34349225dcccea3f86f1d.jpg"



class AFRunMode(Enum):
    """docstring for OAuth2GrandTypes"""
    normal = 10
    batch = 20


ERROR_CODE = {
    400 : "Bad Request 请求出现语法错误",
    401 : "Unauthorized    请求未授权",
    403 : "Forbidden   禁止访问",
    404 : "Not Found   资源未找到",
    405 : "Method Not Allowed  请求方法不适用",
    406 : "Not Acceptable  资源MIME类型不兼容",
    413 : "Request Entity Too Large    请求实体过大",
    429 : "Too Many Requests   请求次数过多或过频繁",
    500 : "Internal Server Error   服务器内部错误",
    503 : "Service Unavailable 服务不可用",
}


class AIFashionFunctions(AFOAuth2):
    """docstring for AIFashionFunctions"""
    API_url_dict = {
        'clothes_detect' : "https://api.aifashion.com/fashion/detect",
        'single_cloth_detect' : "https://api.aifashion.com/fashion/detect-one",
        'clothes_location' : "https://api.aifashion.com/fashion/locate",
        'fashion_tagging' :  "https://api.aifashion.com/fashion/tagging",
        'clothes_naming' : "https://api.aifashion.com/fashion/caption",
        'color_analysis' : "https://api.aifashion.com/fashion/color-analysis",
        'clothes_search_same' : "https://api.aifashion.com/fashion/imgsearch",
        'clothes_search_match' : "https://api.aifashion.com/fashion/mix",
        'body_segment' : "https://api.aifashion.com/human/seg",
        'body_keypoint' : "https://api.aifashion.com/human/keypoints",
        'tag_ocr' : "https://api.aifashion.com/fashion/ocr",
        'clothes_crop' : "https://api.aifashion.com/fashion/crop",
        }


    def __init__(self, client_id=None, client_secret=None, client_filename=None,
                 grant_type=OAuth2GrandTypes.client_credentials, run_mode=AFRunMode.normal,
                 warning=True, debug=False):
        super(AIFashionFunctions, self).__init__(client_id, client_secret, client_filename,
                                                 grant_type, debug=debug)
        self.run_mode = run_mode
        self.warning = warning
        self.debug = debug
        self.__check_function_validity__()


    def __check_function_validity__(self):
        """
        check validity of inputs
        """
        assert self.run_mode == AFRunMode.normal or self.run_mode == AFRunMode.batch, \
            "run mode should be AFRunMode.normal or AFRunMode.batch"
        assert isinstance(self.warning, bool), 'warning should be True/False'
        assert isinstance(self.debug, bool), 'debug should be True/False'


    def __get_af_rsjson(self, func_name, image_url=None, image_fname=None,
                      image_base64=None, **kwargs):
        """
        get response and transform to dict

        input:
            func_name: name of function, using API_url_dict to get final url
            * image_url: url of image
            * image_fname: filename of local image
            * image_base64: base64 string of image

        output:
            if the result is correct, return the data section
        """
        url = self.API_url_dict[func_name]
        if image_url:
            assert re.match(URL_REGEX, image_url), '{0} is not a valid url'.format(image_url)
            payload = kwargs.copy()
            payload.update({"image_url" : image_url})
        else:
            if image_fname:
                assert os.path.exists(image_fname), '{0} does not exist'.format(image_fname)
                with open(image_fname, 'rb') as fd:
                    image_base64 = base64.b64encode(fd.read()).decode()
            if image_base64:
                payload = kwargs.copy()
                payload.update({"image_base64" : image_base64})
        assert payload, "you need to give image_url, image_file or image_base64"
        headers = {
            'authorization' : "Bearer {0}".format(self.token)
        }
        if self.debug:
            print('payload : {0}'.format(payload))
            print('headers : {0}'.format(headers))
        response = requests.request("POST", url, json=payload, headers=headers)
        rjson = json.loads(response.text)
        if self.debug:
            print('reture json : {0}'.format(rjson))
        if not 'code' in rjson:
            raise NotImplementedError(rjson['message'])
        else:
            if rjson['code'] != 100:
                print(ERROR_CODE[rjson['code']])
                if self.debug:
                    print(rjson)
                if self.run_mode == AFRunMode.normal:
                    raise NotImplementedError()
                return None
        return rjson['data']


    def clothes_detect(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [服饰检测](https://developer.aifashion.com/#577c60322c)

    现支持的二级类别包括：上衣(101), 外套(102), 裤子(201), 连衣裙(301),
    半身裙(302), 鞋靴(401), 箱包(501), 类别详细信息，请参照 [常量](https://developer.aifashion.com/#cec3d5c599) 章节。

    0: 未检测到服饰
    1: 上衣
    2: 半身裙
    3: 外套
    4: 连衣裙
    5: 裤子
    6: 鞋
    7: 箱包


    ## HTTP 请求
    POST https://api.aifashion.com/fashion/detect

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码

    image_url、image_base64二选一即可。


    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    objects Array   检测结果数组，数组中每个对象为一件服饰
        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def single_cloth_detect(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [单件服饰检测](https://developer.aifashion.com/#e3ba86f9f1)

    识别图片中一件最显著服饰，并给出检测出服饰的类别、位置和置信度。
    单件服饰识别较多件服饰识别，算法上做了优化，在识别速度和精度上都有很大提升，适用于只需要检测图片中的主要服饰的应用场景，如拍照购物等。
    识别结果和上面多件服饰识别的基本相同，例图如下：

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/detect-one

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]

    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的最显著服饰对象
        """

        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def clothes_location(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [指定服饰定位](https://developer.aifashion.com/#919c2d3050)

    给定数据集中的商品或图片条目，在上传图片中识别出该服饰，并给出位置坐标和置信度。

    指定服饰定位适用于服饰电商看图购、买家秀，时尚内容服饰打点等应用场景。

    例如图片：

    TODO 指定服饰定位图

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/locate

    ## 请求参数
    参数名 参数值类型   描述
    dataset_name    String  数据集名称，用于唯一指定数据集
    product_id  String  条目 product_id，指定数据集中的特定商品
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码

    image_url、image_base64二选一即可。


    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    item    Object  定位到的服饰条目
    location    Object  位置信息
    返回的条目可以是商品条目或图片条目，条目字段的具体定义请参照 商品条目实体 和 图片条目实体。

        """

        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def fashion_tagging(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [时尚标签](https://developer.aifashion.com/#3750f67335)

    为图片中指定的服饰智能打标签，标签内容包括类别和服饰属性等信息。

    例图如下：

    Alt text

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/tagging

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]
    

    image_url、image_base64二选一即可。
    region 可以为空，当 region 为空时默认分析图片中最显著的服饰。


    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的服饰对象
    tags    Array   服饰对象的标签键值对列表

        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def clothes_naming(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [服饰命名](https://developer.aifashion.com/#b687deeb5f)

    为图片中的给定服饰命名，当前支持多种[语言](https://developer.aifashion.com/#83b604e91d)，
    详细情况参照[常量](https://developer.aifashion.com/#cec3d5c599)章节。


    代码  语言  描述
    zh_cn   简体中文
    zh_hk   繁体中文
    en      英文
    ja      日语
    ko      韩语
    fr      法语
    de      德语
    es      西班牙语
    pt      葡萄牙语
    ar      阿拉伯语


    以中文为例，例图如下：

    Alt text

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/caption

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]
    language    String  命名所用语言，默认为 zh_cn
    image_url、image_base64二选一即可。
    region 可以为空，当 region 为空时默认为图片中最显著的服饰命名。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的服饰对象
    caption String  命名结果

        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def color_analysis(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [服饰颜色分析](https://developer.aifashion.com/#5ccae2aa21)

    分析图片中指定服饰的颜色分布，包括颜色 RGB 值、名称和所占比例。

    例如下图：

    TODO 颜色分布图

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/color-analysis

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]
    image_url、image_base64二选一即可。
    region 可以为空，当 region 为空时默认分析图片中最显著服饰。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的服饰对象
    colors  Array   分析出的颜色列表


        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def clothes_search_same(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [搜索同款](https://developer.aifashion.com/#d3fd3e289e)

    在指定数据集中找出和图片中指定服饰外观相似的条目，搜索结果一般都为同类别服饰。

    例图如下：

    Alt text

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/imgsearch

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]
    dataset_name    String  指定数据集进行搜索
    max_results Integer 最多返回条目数，默认值为 20，最小值为 1，最大值为 100
    image_url、image_base64二选一即可。
    region 可以为空，当 region 为空时默认分析图片中最显著服饰。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的服饰对象
    similar_items   Array   搜索到的相似条目
    返回的条目可以是商品条目或图片条目，条目字段的具体定义请参照 商品条目实体 和 图片条目实体。


        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def clothes_search_match(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [搜索搭配](https://developer.aifashion.com/#b415b5e17a)

    在指定数据集中找出和图片中指定服饰外观搭配的条目，搜索结果一般都为跨类别服饰。

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/mix

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待分析区域的相对位置，[x1, y1, x2, y2]
    dataset_name    String  指定数据集进行搭配
    max_results Integer 最多返回条目数，默认值为 20，最小值为 1，最大值为 100
    image_url、image_base64二选一即可。
    region 可以为空，当 region 为空时默认分析图片中最显著服饰。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    object  Object  检测到的服饰对象
    mix_items   Array   搜索到的搭配条目
    返回的条目可以是商品条目或图片条目，条目字段的具体定义请参照 商品条目实体 和 图片条目实体。


        """

        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def body_segment(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    [人像分割](https://developer.aifashion.com/#8924c77173)

    在给定图片中返回人像的像素级分割信息。

    ## HTTP 请求
    POST https://api.aifashion.com/human/seg

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    image_url、image_base64二选一即可。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    segs    list    检测到的人像语义分割信息，面积由大到小排列
    people_num  int 图片中检测到人的个数
    seg 返回值使用方法
    seg信息经过了cocotools进行了编码，成为一个json类型，使用者需要将返回的seg信息进行解码，解码后得到图片的mask掩码。

    以使用cocotools的python接口为例：

    首先安装pycocotools的python接口，

    pip install pycocotools

    使用pycocotools对mask进行编码：

    from pycocotools import mask;
    img_mask_json = mask.encode(img_mask) # img_mask is a np-array mask（背景是0，人像是1）

    使用pycocotools对mask进行解码：

    from pycocotools import mask;
    img_mask = mask.decode(img_mask_json) # img_mask_json 为API中segs列表中每一个对应的json值。


        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def body_keypoint(self, image_url=None, image_fname=None, image_base64=None, **kwargs):
        """
    人体关键点


    https://developer.aifashion.com/#65b5e84a9f


    在给定图片中返回人体的关键点信息。


    人体关键点
    ID  英文名称    中文名称
    0   nose        鼻子
    1   left_eye    左眼
    2   right_eye   右眼
    3   left_ear    左耳
    4   right_ear   右耳
    5   left_shoulder   左肩
    6   right_shoulder  右肩
    7   left_elbow  左肘
    8   right_elbow 右肘
    9   left_wrist  左腕
    10  right_wrist 右腕
    11  left_hip    左臀
    12  right_hip   右臀
    13  left_knee   左膝
    14  right_knee  右膝
    15  left_ankle  左踝
    16  right_ankle 右踝


    ## HTTP 请求
    POST https://api.aifashion.com/human/keypoints

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    image_url、image_base64二选一即可。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    keypoints   list    检测到的人体关键点信息
    people_num  int 图片中检测到人的个数
    关键点的类别信息详见[常量](https://developer.aifashion.com/#cec3d5c599)。

    经验上keypoint置信度在0.80以上为可信预测。


        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def tag_ocr(self, image_url=None, image_fname=None, image_base64=None, **kwargs):

        """
    服饰吊牌OCR

    https://developer.aifashion.com/#ocr

    在给定吊牌图片中返回识别的文字及位置。

    例图如下：

    Alt text

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/ocr

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    image_url、image_base64二选一即可。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    image   Object  图片信息，包括 id、url 以及图的长和宽
    degree  String  文字角度
    text    String  识别的文字
    x_center    Float   文字框横坐标中心点
    y_center    Float   文字框纵坐标中心点
    width   Float   文字框宽度
    height  Float   文字框高度

        """


        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson


    def clothes_crop(self, image_url=None, image_fname=None, image_base64=None, **kwargs):

        """

    服饰智能切图


    https://developer.aifashion.com/#7fd01860b3


    智能分析给定服装图片，给服装的细节抠图。

    例图如下：

    Alt text

    ## HTTP 请求
    POST https://api.aifashion.com/fashion/crop

    ## 请求参数
    参数名 参数值类型   描述
    image_url   String  待识别图片 URL，公网可访问
    image_base64    String  待识别图片二进制数据的 base64 编码
    region  [Float, Float, Float, Float]    待 crop 的服饰区域的相对位置 [x1, y1, x2, y2]
    image_url、image_base64二选一即可。
    ## HTTP 响应结果
    响应结果中主要字段及描述如下：

    字段名 字段值类型   描述
    object  Object  检测到的服饰类别
    image   Object  图片信息，包括 id、url 以及图的长和宽
    name    String  切图的类别
    x   Float   切图框中心点 x 坐标
    y   Float   切图框中心点 y 坐标
    width   Float   切图框宽
    height  Float   切图框高
    confidence  Float   切图置信度


        """
        warnings.warn("This function is just prototype, not complete yet", FutureWarning)
        func_name = sys._getframe().f_code.co_name # acquire function name, for getting URL
        rsjson = self.__get_af_rsjson(func_name, image_url, image_fname, image_base64, **kwargs)
        return rsjson
