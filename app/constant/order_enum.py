from enum import Enum


# 订单状态, 0: 待支付, 1: 待发货, 2: 已发货, 3: 已完成, 4: 已取消
class OrderStatus(Enum):
    PENDING_PAYMENT = 0  # 待支付
    PENDING_SHIPMENT = 1  # 待发货
    SHIPPED = 2  # 已发货
    COMPLETED = 3  # 已完成
    CANCELED = 4  # 已取消

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]


class OrderPayType(Enum):
    WECHAT = 0  # 微信支付
    ALIPAY = 1  # 支付宝支付

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]
