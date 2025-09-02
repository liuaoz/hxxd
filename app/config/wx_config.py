import os

WX_MCH_ID = os.getenv('WX_MCH_ID')
WX_MCH_SERIAL_NO = os.getenv('WX_MCH_SERIAL_NO')
WX_APP_ID = os.getenv('WX_APP_ID')
WX_APP_SECRET = os.getenv('WX_APP_SECRET')
WX_NOTIFY_URL = os.getenv('WX_NOTIFY_URL')
WX_API_V3_KEY = os.getenv('WX_API_V3_KEY')
WX_API_PRIVATE_KEY_PATH = os.getenv('WX_API_PRIVATE_KEY_PATH')
WX_API_PUBLIC_KEY_PATH = os.getenv('WX_API_PUBLIC_KEY_PATH')

JSAPI_URL = os.getenv('JSAPI_URL', 'https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi')
