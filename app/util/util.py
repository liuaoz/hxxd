import uuid


def generate_uuid():
    """
    generate uuid, and return the last 10 characters
    """
    return str(uuid.uuid4()).replace("-", "")[-10:]


def generate_order_no():
    """
    生成一个12位的数字订单号
    """
    return str(uuid.uuid4().int)[:12]  # 取UUID的整数形式的前12位
