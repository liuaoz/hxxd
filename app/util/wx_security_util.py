import base64
import json
from typing import Dict, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from vo.wx.wx_vo import PaySuccessHeader


def _load_private_key(key_path: str) -> rsa.RSAPrivateKey:
    """加载商户私钥"""
    try:
        with open(key_path, 'r') as f:
            private_key_data = f.read()
        return serialization.load_pem_private_key(
            private_key_data.encode(),
            password=None
        )
    except Exception as e:
        raise Exception(f"加载私钥失败: {str(e)}")


def _load_public_key(key_path: str) -> rsa.RSAPublicKey:
    """加载微信支付公钥"""
    try:
        with open(key_path, 'r') as f:
            public_key_data = f.read()
        return serialization.load_pem_public_key(public_key_data.encode())
    except Exception as e:
        raise Exception(f"加载公钥失败: {str(e)}")


def _build_sign_string(method: str, url: str, timestamp: int, nonce: str, body: Optional[Dict] = None) -> str:
    """构建待签名字符串"""
    lines = [
        method.upper(),
        url,
        str(timestamp),
        nonce,
        json.dumps(body, separators=(',', ':'), ensure_ascii=False) if body else ""
    ]
    return '\n'.join(lines) + '\n'


class WeChatPaySecurity:
    """微信支付安全工具类，处理签名和验签"""

    def __init__(self, merchant_private_key_path: str, wechatpay_public_key_path: str):
        """
        初始化微信支付安全工具

        Args:
            merchant_private_key_path: 商户私钥文件路径
            wechatpay_public_key_path: 微信支付公钥文件路径
        """
        self.merchant_private_key = _load_private_key(merchant_private_key_path)
        self.wechatpay_public_key = _load_public_key(wechatpay_public_key_path)

    def create_signature(self, method: str, url: str, timestamp: int,
                         nonce: str, body: Optional[Dict] = None) -> str:
        """
        创建微信支付API请求签名

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            url: 请求URL (不包含域名)
            timestamp: 时间戳 (秒)
            nonce: 随机字符串
            body: 请求体数据 (None表示无请求体)

        Returns:
            Base64编码的签名字符串
        """
        # 构建签名字符串
        sign_str = _build_sign_string(method, url, timestamp, nonce, body)

        # 使用私钥签名
        signature = self.merchant_private_key.sign(
            sign_str.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        # Base64编码签名
        return base64.b64encode(signature).decode('utf-8')

    def verify_wechatpay_signature(self, header: PaySuccessHeader, body: str) -> bool:
        """
        验证微信支付回调的签名

        Args:
            header: 请求头信息
            body: 原始请求体字符串

        Returns:
            bool: 签名是否验证通过
        """
        try:
            # 获取请求头中的签名信息
            signature = header.wechatpay_signature
            serial_no = header.wechatpay_serial
            timestamp = header.wechatpay_timestamp
            nonce = header.wechatpay_nonce

            if not all([signature, serial_no, timestamp, nonce]):
                return False

            # 构建待验证的签名字符串
            sign_message = f"{timestamp}\n{nonce}\n{body}\n"

            # Base64解码签名
            signature_bytes = base64.b64decode(signature)

            # 验证签名
            self.wechatpay_public_key.verify(
                signature_bytes,
                sign_message.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True

        except (InvalidSignature, Exception):
            return False

