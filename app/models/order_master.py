from tortoise import fields

from models import BaseModel


class OrderMaster(BaseModel):
    """
    订单表
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='order_master_user')

    # 订单信息
    order_no = fields.CharField(max_length=20)
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.IntField(description="订单状态, 0: 待支付, 1: 已支付, 2: 已发货, 3: 已完成, 4: 已取消")
    payment_method = fields.IntField(description="支付方式, 0: 微信支付, 1: 支付宝支付")
    payment_time = fields.DatetimeField(null=True)

    # 收获信息
    recipient_name = fields.CharField(max_length=50)
    recipient_phone = fields.CharField(max_length=11)
    recipient_address = fields.CharField(max_length=100)

    class Meta:
        table = "order_master"
