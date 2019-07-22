# ----- coding:utf-8 ------
# 秘钥ID
APP_ID = '20190619000308802' #你的appid
SECRET_KEY = 'gAuBfGBhy7uCY37JtlYk' #你的密钥

# base api url
BASE_URL = 'api.fanyi.baidu.com'
API_URL = '/api/trans/vip/translate'

# 支持语言列表
LANGUAGES = ["auto", "zh", "en", "yue", "wyw", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est", "dan", "fin", "cs", "rom", "slo", "swe", "hu", "cht", "vie"]

# 状态码映射
STATU_CODE_MAP = {
    "52001": "1001",    # 请求超时
    "54000": "1002",    # 必填参数为空
}


# 随机数据最小和最大值，也可另设其它值
RANDOM_LOW = 32768
RANDOM_UP = 65536
