import base64
import json

from Crypto.Cipher import AES

from service.wx_service import code_2_session


def decrypt_user_info(encrypted_data, iv, session_key):
    # Base64 解码
    session_key = base64.b64decode(session_key)
    encrypted_data = base64.b64decode(encrypted_data)
    iv = base64.b64decode(iv)

    # 使用 AES 解密
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    # 去除填充
    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]

    # 解析 JSON 数据
    user_info = json.loads(decrypted_data.decode('utf-8'))
    return user_info


async def login(code, encrypted_data, iv):
    """
    小程序登录
    :param code:
    :param encrypted_data:
    :param iv:
    :return:
    """
    token = None
    # base64 decode
    decoded_bytes = base64.b64decode(encrypted_data)
    iv_bytes = base64.b64decode(iv)
    session = await code_2_session(code)

    if session and session.get("openid"):
        session_key = session.get("session_key")
        user_info = decrypt_user_info(decoded_bytes, iv_bytes, session_key)
        print(user_info)
