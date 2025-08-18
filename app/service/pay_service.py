import time
import uuid

from config.wx_config import WX_MCH_ID, WX_APP_ID, WX_API_PRIVATE_KEY_PATH, WX_NOTIFY_URL, WX_MCH_SERIAL_NO
from util.wxpay_util import WeChatPayUtil


class WxPayService:

    @staticmethod
    async def prepay(out_order_no: str, amount: int, openid: str, description: str):
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

        pay_util = WeChatPayUtil(WX_MCH_ID, WX_MCH_SERIAL_NO, WX_API_PRIVATE_KEY_PATH)

        resp = pay_util.post('https://api.mch.weixin.qq.com', '/v3/pay/transactions/jsapi', body)

        if resp.status_code != 200:
            raise Exception(f"预支付失败: {resp.text}")

        data = resp.json()
        prepay_id = data['prepay_id']

        time_stamp = int(time.time())
        nonce_str = str(uuid.uuid4()).replace('-', '')

        pay_sign = pay_util.do_sign(pay_util.build_message(time_stamp, nonce_str, prepay_id))

        return {
            "package": f'prepay_id={prepay_id}',
            "time_stamp": time_stamp,
            "nonce_str": nonce_str,
            "pay_sign": pay_sign,
            "sign_type": "RSA"
        }
