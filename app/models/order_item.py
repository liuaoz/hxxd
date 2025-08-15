from tortoise import fields

from models import BaseModel


class OrderItem(BaseModel):
    """
    订单详情表
    """
    order = fields.ForeignKeyField('models.Order', related_name='order_item_order')
    product = fields.ForeignKeyField('models.Product', related_name='order_item_product')

    product_title = fields.CharField(max_length=50)
    product_main_file_id = fields.IntField()
    quantity = fields.IntField(description="商品数量")
    price = fields.IntField(description="商品价格, 单位: 分")

    class Meta:
        table = "order_item"
