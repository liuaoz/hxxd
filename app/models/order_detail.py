from tortoise import fields

from models import BaseModel


class OrderDetail(BaseModel):
    """
    订单详情表
    """
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField('models.OrderMaster', related_name='order_detail_order_master')
    goods = fields.ForeignKeyField('models.Goods', related_name='order_detail_goods')
    goods_title = fields.CharField(max_length=50)
    goods_image = fields.TextField()
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "order_detail"
