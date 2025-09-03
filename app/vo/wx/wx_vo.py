from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PaySuccessHeader(BaseModel):
    wechatpay_serial: str
    wechatpay_signature: str
    wechatpay_timestamp: str
    wechatpay_nonce: str


class WechatPayResource(BaseModel):
    """微信支付通知资源数据"""
    algorithm: str
    ciphertext: str
    associated_data: Optional[str]
    nonce: str
    original_type: str


class WechatPayNotify(BaseModel):
    """微信支付通知主体"""
    id: str
    create_time: datetime
    event_type: str
    summary: str
    resource_type: str
    resource: WechatPayResource


# {"mchid":"1550938701","appid":"wx3155c0d75306acc8","out_trade_no":"133868975711_2","transaction_id":"4200002800202509027966147114"
# ,"trade_type":"JSAPI","trade_state":"SUCCESS","trade_state_desc":"支付成功","bank_type":"OTHERS","attach":"","success_time":"2025-09-02T22:01:31+08:00"
# ,"payer":{"openid":"owJBV43C3ugI76lqpuFpzWQt7o3c"}
# ,"amount":{"total":1,"payer_total":1,"currency":"CNY","payer_currency":"CNY"}}

class Payer(BaseModel):
    openid: str


class DecryptedData(BaseModel):
    """解密后的支付数据"""
    appid: str
    mchid: str
    out_trade_no: str
    transaction_id: Optional[str]
    trade_type: Optional[str]
    trade_state: str
    trade_state_desc: str
    bank_type: Optional[str]
    attach: Optional[str]
    success_time: Optional[datetime]
    payer: dict
    amount: dict
    scene_info: Optional[dict] = None
    promotion_detail: Optional[list[dict]] = None
