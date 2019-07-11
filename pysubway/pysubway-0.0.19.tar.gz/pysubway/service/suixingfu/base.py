import json
import time
from typing import Dict, Any

import requests
from Crypto.Hash import SHA

try:
    from utils.encryption.rsa2 import RSAEncryption
    from utils.encryption.des import DES
    from utils.ustring import unique_id
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.utils.encryption.rsa2 import RSAEncryption
    from pysubway.utils.encryption.des import DES
    from pysubway.utils.ustring import unique_id


class SuixingfuBase:

    def __init__(self, des_key: str, rsa_prv_key: str, url: str, channel_number: str):
        self.des_key = des_key
        self.rsa_prv_key = rsa_prv_key
        self.url = url
        self.channel_number = channel_number

    def gen_sign(self, send_data: Dict[str, str]) -> str:
        """
        对Base64编码后的reqData密文使用合作方RSA私钥进行签名，
        将签名结果用Base64编码后得到签名串，将签名串放置到报文头的sign字段中，请求报文构造完成发送。
        sign=$(self.reqData -> RSA私钥进行签名 -> Base64编码)
        :return:
        """
        return RSAEncryption.gen_signature(self.gen_req_data(send_data)['reqData'], self.rsa_prv_key, hash_type=SHA)

    def gen_order_num(self) -> str:
        return str(unique_id())

    def gen_header(self, sign: str, order_num: str, timestamp: str = time.strftime('%Y%m%d%H%M%S')) -> Dict[str, Any]:
        return dict(
            channelNo=self.channel_number,
            orderNo=order_num,
            sign=sign,
            timeStamp=timestamp,
        )

    def gen_req_data(self, send_data: Dict[str, Any]) -> Dict[str, str]:
        jsonify = json.dumps(send_data)
        req_data = DES.encrypt(jsonify, self.des_key)
        return {
            'reqData': req_data
        }

    def _request(self, req_data: Dict[str, str], header: Dict[str, str]) -> Dict[str, str]:
        """
        注意 headers 和传值方式，和随行付文档中的完全不一致；
        :param orderNo: 请求订单号, 每次请求必须是唯一值，标明此报文的唯一编号
        :return:
        """
        response = requests.post(self.url, headers=header, data=req_data)
        if not response.ok:
            raise ValueError(
                f'response.content {response.content} response.status_code {response.status_code} is invalid')
        return response.json()

    def request(self, send_data: Dict[str, str]) -> Dict[str, str]:
        req_data = self.gen_req_data(send_data)
        sign = self.gen_sign(send_data)
        order_num = self.gen_order_num()
        header = self.gen_header(sign, order_num)
        return self._request(req_data, header)
