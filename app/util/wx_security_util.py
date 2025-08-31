import base64
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import Request, HTTPException, status

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


# 全局支付安全工具实例
# 在实际应用中，这些路径应该从配置文件中读取
wechat_pay_security = WeChatPaySecurity(
    merchant_private_key_path="path/to/merchant_private_key.pem",
    wechatpay_public_key_path="path/to/wechatpay_public_key.pem"
)


@app.post("/wechatpay/callback")
async def wechatpay_callback(request: Request):
    """
    微信支付回调接口
    验证签名并处理支付结果通知
    """
    # 读取原始请求体
    body = await request.body()

    # 验证签名
    if not wechat_pay_security.verify_wechatpay_signature(request, body):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="签名验证失败"
        )

    try:
        # 解析通知内容
        notification = json.loads(body.decode())

        # 处理支付结果（这里只是示例，实际应该进行业务处理）
        # 例如：更新订单状态、发货等

        # 返回成功响应（微信支付要求返回特定格式）
        return {
            "code": "SUCCESS",
            "message": "成功"
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的JSON格式"
        )


@app.post("/create-payment")
async def create_payment(order_data: Dict[str, Any]):
    """
    创建支付订单接口
    生成带签名的支付参数
    """
    try:
        # 生成必要参数
        timestamp = int(datetime.now().timestamp())
        nonce = hashlib.md5(str(timestamp).encode()).hexdigest()[:16]
        method = "POST"
        url = "/v3/pay/transactions/jsapi"

        # 创建签名
        signature = wechat_pay_security.create_signature(
            method=method,
            url=url,
            timestamp=timestamp,
            nonce=nonce,
            body=order_data
        )

        # 构建授权信息（用于微信支付API请求头）
        merchant_id = "your_merchant_id"  # 实际应该从配置获取
        serial_no = "your_certificate_serial_no"  # 证书序列号

        authorization = (
            f'WECHATPAY2-SHA256-RSA2048 '
            f'mchid="{merchant_id}",'
            f'nonce_str="{nonce}",'
            f'signature="{signature}",'
            f'timestamp="{timestamp}",'
            f'serial_no="{serial_no}"'
        )

        return {
            "authorization": authorization,
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": signature
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建支付失败: {str(e)}"
        )


# 工具函数端点
@app.get("/tools/sign")
async def sign_data(
        method: str,
        url: str,
        timestamp: int,
        nonce: str,
        body: Optional[str] = None
):
    """
    签名工具端点（用于测试和调试）
    """
    try:
        body_dict = json.loads(body) if body else None
        signature = wechat_pay_security.create_signature(
            method=method,
            url=url,
            timestamp=timestamp,
            nonce=nonce,
            body=body_dict
        )
        return {"signature": signature}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"签名失败: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
