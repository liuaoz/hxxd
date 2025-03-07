import logging
from datetime import timedelta, datetime

import jwt

from config.jwt_config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION


def generate_token(payload: dict):
    """
    * JwtToken生成的工具类
    :param payload:
    :return:
    """
    payload.update({
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION)
    })
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        logging.error(f'Verify token error: {e}')
        return None
