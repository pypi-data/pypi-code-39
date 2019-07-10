# coding:utf-8
from urllib import request


def send_msg(mobile, title, body,
             url="http://127.0.0.1:8001/v1/sms/send",
             usr="znsy",
             pwd="ynkg2019"):
    """
    向短信网关发送SMS信息
    :param usr:
    :param pwd:
    :param mobile:
    :param body:
    :return:
    """
    if title == '' or title is None:
        raise ValueError(u'短信标题不能为空！')

    if body == '' or body is None:
        raise ValueError(u'短信内容不能空!')

    req = request.Request(url, data={
        'user': usr,
        'pwd': pwd,
        'number': mobile,
        'content': "【%s】%s" % (title, body)
    }, method='POST')

    return request.urlopen(req)
