import logging

import requests

from config.wx_config import WX_APP_ID, WX_APP_SECRET

BASE_URL = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"


async def code_2_session(code: str):
    """
    通过code获取session_key
    :param code: 小程序登录时获取的code
    :return: openid, session_key, unionid, errcode, errmsg
    """
    url = BASE_URL % (WX_APP_ID, WX_APP_SECRET, code)
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    logging.error("code_2_session error: %s", resp.text)
    return None
