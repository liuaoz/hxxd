import time
import uuid
import json
import base64
import requests

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class WeChatPayUtil:
    def __init__(self, mchid: str, serial_no: str, private_key_path: str):
        """
        :param mchid: 商户号
        :param serial_no: 商户证书序列号（从商户平台 API 证书详情里获取）
        :param private_key_path: 商户私钥路径 (apiclient_key.pem, PKCS#8 格式)
        """
        self.mchid = mchid
        self.serial_no = serial_no
        self.private_key = self._load_private_key(private_key_path)

    def _load_private_key(self, path: str):
        """加载 PEM 私钥"""
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def sign(self, method: str, url_path: str, body: str, timestamp: str, nonce_str: str) -> str:
        """生成签名字符串"""
        message = f"{method}\n{url_path}\n{timestamp}\n{nonce_str}\n{body}\n"

        signature = self.private_key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode("utf-8")

    def build_authorization(self, method: str, url_path: str, body: dict) -> (dict, str):
        """
        生成请求头和序列化后的 body
        :param method: HTTP 方法 (如 POST/GET)
        :param url_path: 接口路径 (如 /v3/pay/transactions/jsapi)
        :param body: 请求体 dict，如果 GET 请求传 {}
        """
        timestamp = str(int(time.time()))
        nonce_str = str(uuid.uuid4())
        body_str = json.dumps(body, separators=(",", ":")) if body else ""

        signature = self.sign(method, url_path, body_str, timestamp, nonce_str)

        authorization = (
            f'WECHATPAY2-SHA256-RSA2048 '
            f'mchid="{self.mchid}",'
            f'nonce_str="{nonce_str}",'
            f'signature="{signature}",'
            f'timestamp="{timestamp}",'
            f'serial_no="{self.serial_no}"'
        )

        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return headers, body_str

    def post(self, url: str, url_path: str, body: dict):
        """发起 POST 请求（自动带签名）"""
        headers, body_str = self.build_authorization("POST", url_path, body)
        return requests.post(url + url_path, headers=headers, data=body_str)

    def get(self, url: str, url_path: str, params: dict = None):
        """发起 GET 请求（自动带签名）"""
        headers, _ = self.build_authorization("GET", url_path, {})
        return requests.get(url + url_path, headers=headers, params=params)
