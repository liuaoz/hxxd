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
    scene_info: Optional[dict]
    promotion_detail: Optional[list[dict]]
