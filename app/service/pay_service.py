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
        return data['prepay_id']
