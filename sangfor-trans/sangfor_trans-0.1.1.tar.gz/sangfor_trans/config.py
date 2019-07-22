# --*-- coding: utf-8 --*--

# 翻译器（翻译类型）
BAIDU = "baidu"
GOOGLE = "google"
# SOGOU = "sogou"
# YOUDAO = "youdao"

# 状态码和状态信息
SUCCESS_STATUE_CODE = "1000"                                # 成功
PARAM_STATUE_CODE = "1002"                                  # 必填参数为空
EXCEPT_STATU_CODE = "1003"                                  # 其它异常情况
INVALID_TRANS_TYPE = "INVALID TRANSLATE TYPE"               # 传入的翻译类型有误
INVALID_SOURCE_LANG = "INVALID SOURCE LANGUAGE"             # 传入的源语言参数有误
INVALID_DEST_LANG = "INVALID DESTINATION LANGUAGE"          # 传入的译文语言参数有误
INVALID_PARAMETER = "FROM_LANG OR TO_LANG OR QUERY_TEXT IS NONE"           # 传入的需翻译text有误

SUCCESS = "SUCCESS"

LANGMAP = {
    'zh': 'zh-cn',  # 中文
    'vie': 'vi',    # 越南语
    'cht': 'zh-tw', # 繁体中文
    'swe': 'sv',    # 瑞典语
    'rom': 'ro',    # 罗马尼亚语
    'fra': 'fr',    # 法语
    'jp': 'ja',     # 日语
    'kor': 'ko',    # 韩语
    'spa': 'es',    # 西班牙语
    'ara': 'ar',    # 阿拉伯语
    'bul': 'bg',    # 保加利亚语
    'est': 'et',    # 爱沙尼亚语
    'dan': 'da',    # 丹麦语
    'fin': 'fi',    # 芬兰语
    'sol': 'sl'     # 斯洛文尼亚语
}

# LANGMAP的key和value转换
LANGMAP_REVERSED = dict(map(reversed, LANGMAP.items()))