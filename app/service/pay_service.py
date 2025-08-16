import base64
import json
import random
import string
import time

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from config.wx_config import WX_MCH_ID, WX_APP_ID, JSAPI_URL, WX_API_PRIVATE_KEY_PATH, WX_NOTIFY_URL
from constant.url_constant import URL_ORDER_PAY_SUCCESS_NOTIFY


class WxPayService:

    @staticmethod
    async def generated_pay_sign(package: str, sign_type: str = "RSA"):
        """
        :param package: 预支付包
        :param sign_type: 签名类型，默认RSA
        生成支付签名
        :return: 支付签名
        {
          "sign": "签名字符串"
        }
        """
        time_stamp = str(int(time.time()))
        nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

        sign_data = {
            "appid": WX_APP_ID,
            "timeStamp": time_stamp,
            "nonceStr": nonce_str,
            "package": package,
            "signType": sign_type
        }

        sorted_keys = sorted(sign_data.keys())

        string_to_sign = '\n'.join([f'{key}={sign_data[key]}' for key in sorted_keys]) + '\n'

        # 加载私钥
        rsa_key = RSA.import_key(WX_API_PRIVATE_KEY_PATH)

        # 创建签名对象
        h = SHA256.new(string_to_sign.encode('utf-8'))
        signer = pkcs1_15.new(rsa_key)

        # 生成签名
        signature = signer.sign(h)

        # Base64编码签名
        sign = base64.b64encode(signature).decode('utf-8')

        # 返回所有参数和签名
        result = sign_data.copy()
        result['paySign'] = sign
        return result

    @staticmethod
    async def prepay(out_order_no: str, amount: int, openid: str, description: str):
        """
        预支付接口
        :param out_order_no: 订单ID
        :param amount: 总金额（单位：分）
        :param openid: 用户的openid
        :param description: 订单描述
        :return: 预支付信息
        {
          "prepay_id" : "wx201410272009395522657a690389285100"
        }
        """

        headers = {
            'Authorization': 'WECHATPAY2-SHA256-RSA2048 ',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        body = {
            'appid': WX_APP_ID,
            'mchid': WX_MCH_ID,
            'description': description,
            'out_trade_no': out_order_no,
            'notify_url': WX_NOTIFY_URL,
            'amount': {
                'total': amount,
                'currency': 'CNY'
            },
            'payer': {
                'openid': openid
            }
        }

        response = requests.post(JSAPI_URL, data=json.dumps(body), headers=headers)

        if response.status_code != 200:
            raise Exception(f"预支付失败: {response.text}")
        data = response.json()
        if 'prepay_id' not in data:
            raise Exception("预支付响应中缺少 prepay_id")
        return data['prepay_id']
