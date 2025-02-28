import jwt
from config.jwt_config import JWT_SECRET, JWT_EXPIRATION, JWT_ALGORITHM


def generate_token(payload: dict):
    """
    * JwtToken生成的工具类
    :param payload:
    :return:
    """
    payload.update({
        'exp': JWT_EXPIRATION
    })
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
