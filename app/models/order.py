from tortoise import fields

from models import BaseModel


class Order(BaseModel):
    """
    订单表
    """
    user = fields.ForeignKeyField('models.User', related_name='order_user')

    # 订单信息
    order_no = fields.CharField(max_length=20)
    out_trade_no = fields.CharField(max_length=50, null=True, description="外部交易号, 用于支付平台的订单号")
    total_amount = fields.IntField(description="订单总金额, 单位: 分")
    status = fields.IntField(description="订单状态, 0: 待支付, 1: 待发货, 2: 已发货, 3: 已完成, 4: 已取消", default=0)

    # 支付信息
    payment_type = fields.IntField(description="支付方式, 0: 微信支付, 1: 支付宝支付")
    payment_time = fields.DatetimeField(null=True)

    # 收获信息
    recipient_name = fields.CharField(max_length=50)
    recipient_phone = fields.CharField(max_length=11)
    recipient_address = fields.CharField(max_length=100)

    class Meta:
        table = "order"
